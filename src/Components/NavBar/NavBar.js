import './NavBar.css';
import React from 'react';
import { Button } from '../Button/Button';

const tabs = ["US", "World", "Politics", "Business", "Health", "Entertainment", "Opinion"];


export class NavBar extends React.Component {
  constructor(props) {
    super(props);
  }

  createTabButtons() {
    return (tabs.map((word) => <Button handleOnClick={this.props.onButtonClick} text={word} />));
  }

  render() {
    return (
      <nav>
        <ul>
          {this.createTabButtons()}
        </ul>
      </nav>
    );
  }
}