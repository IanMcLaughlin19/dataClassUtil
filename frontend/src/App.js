import logo from './logo.svg';
import './App.css';
import TextEditor from "./components/textEditor";

function App() {
  return (
    <div className="App">
      <header className="App-header">
          <h1>JSON 2 Python Data Classes</h1>
      </header>
        <h2>
            <p className="paragraph">
                This is a JSON to Python data structure converter. This is useful for quickly going to from working with
                an API response to having a nested data structure that can be worked with easily. It allows programmers to
                write code that remembers the complex data structures their working with, so when they come back to the
                code later or share it with other, no additional references are needed. It can also prevent code debugging issues
                where you are dealing with a series of nested dicts and can't figure out why a specific KeyError or something
                similar is getting thrown. The source code for this project is at https://github.com/ianm199/dataClassUtil.
            </p>
        </h2>
        <h3>
        <div>
            <TextEditor />
        </div>
        </h3>
    </div>
  );
}

export default App;
