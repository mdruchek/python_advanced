import random

from flask import Flask, request, jsonify
from celery import Celery, group
import time

app = Flask(__name__)

# Конфигурация Celery
celery_app = Celery(
    app.name,
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)


# Задача Celery для обработки изображения
@celery_app.task
def process_image(image_id):
    # В реальной ситуации здесь может быть обработка изображения
    # В данном примере просто делаем задержку для демонстрации
    time.sleep(random.randint(100, 110))
    return f'Image {image_id} processed'


@app.route('/process_images', methods=['POST'])
def process_images():
    images = request.json.get('images')

    if images and isinstance(images, list):
        # Создаем группу задач
        task_group = group(
            process_image.s(image_id)
            for image_id in images
        )

        # Запускаем группу задач и сохраняем ее
        result = task_group.apply_async()
        result.save()

        # Возвращаем пользователю ID группы для отслеживания
        return jsonify({'group_id': result.id}), 202
    else:
        return jsonify({'error': 'Missing or invalid images parameter'}), 400


@app.route('/status/<group_id>', methods=['GET'])
def get_group_status(group_id):
    result = celery_app.GroupResult.restore(group_id)

    if result:
        # Если группа с таким ID существует,
        # возвращаем долю выполненных задач
        status = result.completed_count() / len(result)
        return jsonify({'status': status}), 200
    else:
        # Иначе возвращаем ошибку
        return jsonify({'error': 'Invalid group_id'}), 404


@app.route('/cancel/<group_id>', methods=['GET'])
def canceling_task_group(group_id):
    celery_app.control.revoke(group_id)
    return jsonify({'canceling_task_group': group_id})


@app.route('/control')
def control_task():
    reg = celery_app.control.inspect(timeout=10.0).registered()
    stats = celery_app.control.inspect(timeout=10.0).stats()
    return jsonify(reg, stats)


if __name__ == '__main__':
    app.run(debug=True)
