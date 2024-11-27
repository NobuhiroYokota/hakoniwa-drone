const express = require('express');
const { exec } = require('child_process');
const os = require('os'); // OS判定用
const cors = require('cors');

const app = express();
const PORT = 5000;

app.use(cors());

app.post('/run-batch', (req, res) => {
  const batchFilePath = './lib/run-test.bat'; // バッチファイルの相対パス
  let command;

  if (os.platform() === 'win32') {
    // Windows 用コマンド
    command = `start "" "${batchFilePath}"`;
  } else {
    // Linux/macOS 用コマンド
    command = `sh "${batchFilePath}"`; // または `./${batchFilePath}`（実行権限がある場合）
  }

  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${error.message}`);
      return res.status(500).send('バッチファイルの実行に失敗しました');
    }
    if (stderr) {
      console.error(`Stderr: ${stderr}`);
    }
    console.log(`Stdout: ${stdout}`);
    res.send('バッチファイルを実行しました');
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
