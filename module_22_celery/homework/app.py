"""
В этом файле будет ваше Flask-приложение
"""

from typing import List

from flask import Flask, jsonify, request

from celery_ import chord, celery_app, r, process_image, archiving_and_send_email_results
from functions import get_emails_from_csv, adding_data_to_csv, deleting_data_from_csv
from config import MAILING_LIST_FILE

from celery.result import AsyncResult

app = Flask(__name__)


@app.route('/blur', methods=['POST'])
def blur():
    """
    Ставит в очередь обработку переданных изображений. Возвращает ID задачи.
    """
    request_data = request.files
    email = request.form.get('email')
    images = request_data.getlist('images')
    files_names = []
    for image in images:
        files_names.append(image.filename)
        image.save(image.filename)
    if images and isinstance(images, List):
        header = (process_image.s(image) for image in files_names)
        callback = archiving_and_send_email_results.s(email=email)
        result = chord(header)(callback)
        result.parent.save()
        r.hset(result.id, mapping={
            'result_total': result.id,
            'result_process_images': result.parent.id
        })
        return jsonify({'group_id': result.id}), 202
    else:
        return jsonify({'error': 'Missing or invalid images parameter'}), 400


@app.route('/status/<task_id>', methods=['GET'])
def get_task_status(task_id: str):
    """
    Возвращает информацию о задаче: прогресс (количество обработанных задач) и статус (в процессе обработки, обработано, отправлено на почту)
    """
    task_data = r.hgetall(task_id)
    result_total = AsyncResult(app=celery_app, id=task_data['result_total'])
    result_process_images = celery_app.GroupResult.restore(task_data['result_process_images'])

    if result_total.successful():
        status = 'send to the email'
    elif result_process_images.completed_count() == len(result_process_images):
        status = 'processed'
    else:
        status = 'during processing'

    if result_process_images:
        progress = f'{result_process_images.completed_count()} / {len(result_process_images)}'
        return jsonify({'progress': progress, 'status': status}), 200
    else:
        return jsonify({'error': 'Invalid group_id'}), 404


@app.route('/subscribe', methods=['POST'])
def subscribe():
    """
    Пользователь указывает почту и подписывается на рассылку. Каждую неделю ему будет приходить письмо о сервисе на почту.
    """
    user_data: dict = request.json
    emails = get_emails_from_csv(MAILING_LIST_FILE)
    if user_data.get('email') not in emails:
        adding_data_to_csv(MAILING_LIST_FILE, user_data)
        return jsonify({'message': f'{user_data.get("username")} успешно добавлен в список рассылки'})
    return jsonify({'message': f'Пользователь с email {user_data.get("email")} уже получает рассылку'})


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    """
    Пользователь указывает почту и отписывается от рассылки.
    """
    request_data: dict = request.json
    email = request_data.get('email')
    if deleting_data_from_csv(MAILING_LIST_FILE, email):
        return jsonify({'message': f' Пользователь с email {email} успешно удалён из списка рассылки'})
    return jsonify({'message': f'Пользователь с email {email} не найден в списке рассылки'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
