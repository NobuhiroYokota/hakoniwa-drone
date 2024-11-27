document.addEventListener('DOMContentLoaded', () => {
  const statusMessage = document.createElement('p');
  statusMessage.id = 'statusMessage';
  document.body.appendChild(statusMessage);

  statusMessage.textContent = "コース1を開始します...";

  // コース1が選ばれた時の処理
  fetch('http://localhost:5000/run-course1', {
    method: 'POST',
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('コース1の実行に失敗しました');
      }
      return response.text();
    })
    .then(data => {
      statusMessage.textContent = data;
    })
    .catch(error => {
      statusMessage.textContent = `エラー: ${error.message}`;
    });
});
