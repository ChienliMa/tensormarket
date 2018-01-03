import React from "react";
import { observable, computed } from "mobx";
import {observer} from 'mobx-react';

const INPUT = "input";
const OUTPUT = "output";

class Row extends React.Component {
  constructor(props){
    super(props);
    this.state = {}
    this.state.type = props.type;
    this.state.key = props.index;
  }

  render(){
    return (
      <tr>
        <td><input type="text" name={this.state.type + this.state.key + "name"} placeholder="name your input"/></td>
        <td><input type="number" name={this.state.type + this.state.key + "width"} placeholder="width"/></td>
        <td><input type="number" name={this.state.type + this.state.key + "height"} placeholder="height"/></td>

        <td>
          <select name={this.state.type + this.state.key + "datatype"}>
            <option value="int32">int32</option>
            <option value="int64">int64</option>
            <option value="float32">float32</option>
            <option value="float64">float64</option>
          </select>

        </td>
        <td><input type="text" name={this.state.type + this.state.key + "desc"} placeholder="describe your input"/></td>
      </tr>
    );
  }
}

@observer
class IOMetaDataForm extends React.Component{
  constructor(props) {
    super(props);
    this.type = props.type;
    this.row_count = observable(1);
  }

  addRow() {
    this.row_count += 1;
  }

  @computed get rowIds() {
    return [...Array(this.row_count).keys()]
  }

  renderRows (){
    return (
      <tbody>{this.rowIds.map((id, index) => <Row type={this.type} key={id} index={id}></Row>)}</tbody>
    );
  }

  render () {
    return (
      <div>
        <p>
          <label>Inputs</label>
        </p>

        <table>
          <tbody>
            <tr>
              <th>label</th>
              <th>width</th>
              <th>height</th>
              <th>datatype</th>
              <th>desc</th>
            </tr>
          </tbody>

          {this.renderRows()}
        </table>
        <button  type="button" onClick={this.addRow.bind(this)}>Add Row</button>

      </div>
    )
  }
}


class UploadForm extends React.Component{
  constructor(props) {
    super(props);
    this.state = {};
    this.state.input_count = 2;
    this.state.output_count = 1;
  }

  render() {
    return (
      <form action = "http://localhost:5000/upload" method = "POST"
            encType = "multipart/form-data">
        <p>
          <label>select model file: </label>
          <input type = "file" name = "file" />
        </p>

        <p>
          <label>Username: </label>
          <input type="text" name = "username" placeholder="separate labels with spaces"/>
        </p>

        <p>
          <label>Model Name: </label>
          <input type="text" name = "model_name" placeholder="separate labels with spaces"/>
        </p>

        <p>
          <label>Signature Key: </label>
          <input type="text" name = "signature_key" placeholder="separate labels with spaces"/>
        </p>

        <IOMetaDataForm type={INPUT}/>
        <IOMetaDataForm type={OUTPUT}/>

        <input type = "submit"/>
      </form>
    )
  }

}

export default UploadForm;