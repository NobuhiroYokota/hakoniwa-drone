const express = require('express');
const { exec } = require('child_process');
const os = require('os');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = 5000;

app.use(cors());

app.post('/run-batch', (req, res) => {
  const batchFilePath = path.join(__dirname, 'run-test.bat'); // 絶対パスを使用
  let command;

  if (os.platform() === 'win32') {
    // start コマンドを使用して新しいプロセスを開始
    command = `start "" "${batchFilePath}"`;
  } else {
    // Linux/macOS 用コマンド（必要に応じて）
    command = `sh "${batchFilePath}"`;
  }

  exec(command, (error, stdout, stderr) => {
    console.log('stdout:', stdout);
    console.error('stderr:', stderr);

    if (error) {
      console.error(`Error: ${error.message}`);
      return res.status(500).send('バッチファイルの実行に失敗しました');
    }
    res.send('バッチファイルを実行しました');
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
