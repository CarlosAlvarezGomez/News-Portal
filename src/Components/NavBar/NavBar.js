import './NavBar.css';
import React from 'react';
import { Button } from '../Button/Button';

const tabs = ["US", "World", "Politics", "Business", "Health", "Entertainment", "Opinion"];

const createTabButtons = (setCategory) => {
  return (tabs.map((word) => Button(setCategory, word)));
}

export const NavBar = (setCategory) => {

    return (
      <nav>
        <ul>
          {createTabButtons(setCategory)}
        </ul>
      </nav>
    );
}