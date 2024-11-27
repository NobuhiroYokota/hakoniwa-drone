import './App.css'

function App() {
  const runBatchFile = async () => {
    try {
      const response = await fetch('http://localhost:5000/run-batch', {
        method: 'POST',
      });
      if (response.ok) {
        alert('バッチファイルを実行しました');
      } else {
        alert('バッチファイルの実行に失敗しました');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('エラーが発生しました');
    }
  };

  return (
    <div>
      <button onClick={runBatchFile}>バッチファイルを実行</button>
    </div>
  );
}

export default App
