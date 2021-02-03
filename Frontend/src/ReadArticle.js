import React from 'react';
import './ReadArticle.css';
import { NavBar } from './Components/NavBar/NavBar';

const ReadArticle  = () => {
  
  const urlParams = window.location

  return (
      <div>
        <section className="heading">
          <h1>NEWS-PORTAL</h1>
          <div className="navBar">
            {NavBar()}
          </div>
        </section>
        <iframe src="https://cornellsun.com/2020/12/17/editorial-cornell-administrators-must-advocate-for-their-marginalized-students"/>
      </div>
    );
}

export default ReadArticle;
