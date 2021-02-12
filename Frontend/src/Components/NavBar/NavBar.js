import './NavBar.css';
import React from 'react';
import { Button } from '../Button/Button';

const tabs = ["US", "World", "Politics", "Business", "Health", "Entertainment", "Opinion"];

// Goes through each tab and creates a button item in the <ul>
const createTabButtons = () => {
  return (tabs.map((word) => Button(word)));
}

export const NavBar = () => {

    return (
      <nav>
        <ul>
          {createTabButtons()}
        </ul>
      </nav>
    );
}