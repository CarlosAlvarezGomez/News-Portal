import './NavBar.css';
import React from 'react';
import { Button } from '../Button/Button';

const tabs = ["US", "World", "Politics", "Business", "Health", "Entertainment", "Opinion"];

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