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
        <iframe src="https://www.dailymail.co.uk/news/article-9217377/Joe-Jill-Biden-pay-respects-Officer-Brian-Sicknick-lies-honor-Capitol.html"/>
      </div>
    );
}

export default ReadArticle;
