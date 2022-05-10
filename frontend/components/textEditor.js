import React, { Component } from 'react';
import { Editor } from 'react-draft-wysiwyg';
import 'react-draft-wysiwyg/dist/react-draft-wysiwyg.css';
import { EditorState, convertToRaw } from 'draft-js';
import "ace-builds";
import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/theme-github";
import "ace-builds/src-noconflict/ext-language_tools";
import "ace-builds/webpack-resolver";
import AceEditor  from 'react-ace';

export default class TextEditor extends Component {

    state = {
        editorState: EditorState.createEmpty(),
        pythonEditorState: EditorState.createEmpty(),
        pythonCode: "",
        classname: "",
        includeSubclassCode: false
    }

    onEditorStateChange = (editorState) => {
        this.setState({
            editorState,
        });
    };

    handleTextChange = (classname) => {
        console.log("TEXT CHANGE")
        this.setState({
            'classname': classname,
        });
    }

    updatePython = (newCode) => {
        console.log("TEST!")
        console.log("NEW CODE")
        console.log(newCode)
        this.setState({pythonCode: newCode}, function () {
            console.log("logging truth")
            console.log(this.state.pythonCode)
        })
    }

    onPythonEditorStateChange = (pythonEditorState) => {
        this.setState({
            pythonEditorState
        })
    }

    onButtonClick = (editorState) => {
        var xhr = new XMLHttpRequest();
        xhr.addEventListener('load', () => {
            console.log(xhr.responseText)
        });
        var url = `https://2otbdflyea.execute-api.us-east-1.amazonaws.com/hello?text=${convertToRaw(editorState.getCurrentContext())}`
        if (this.state.classname) {
            url += `&class_name=${this.state.classname}`
        }
        xhr.open('POST', url);
        xhr.send();
    }

    render() {
        const { editorState, classname } = this.state;
        const onButtonClick = () => {
            var xhr = new XMLHttpRequest();
            xhr.addEventListener('load', () => {
                this.updatePython(JSON.parse(xhr.responseText).text)
            });
            console.log(convertToRaw(editorState.getCurrentContent()).blocks[0].text);
            xhr.open('POST', `https://2otbdflyea.execute-api.us-east-1.amazonaws.com/hello?text=${convertToRaw(editorState.getCurrentContent()).blocks[0].text}`);
            xhr.send();
            this.updatePython(xhr.responseText);
        }
        return (
            <div>
                <div className="jsonEditorBox">
                    <button onClick={onButtonClick}>Submit!</button>
                    <input type="text" defaultValue="" onChange={this.handleTextChange}/>
                    <input type="checkbox" name="includeSubclassCode" value={this.state.includeSubclassCode} />
                <Editor
                    editorState={editorState}
                    toolbarClassName="jsonToolbar"
                    wrapperClassName="jsonWrapper"
                    editorClassName="jsonEditorClass"
                    onEditorStateChange={this.onEditorStateChange}
                />
                </div>
                <div>
                    <AceEditor
                    mode="python"
                    theme="github"
                    name="pythonTextEditor"
                    editorProps={{ $blockScrolling: true }}
                    setOptions={{
                        enableBasicAutocompletion: true,
                        enableLiveAutocompletion: true,
                        enableSnippets: true,
                        width: '900px'
                    }}
                    value={this.state.pythonCode}
                    />
                </div>

            </div>
        )
    }
}