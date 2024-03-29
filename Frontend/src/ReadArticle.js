import React from 'react';
import { useState } from 'react';
import './ReadArticle.css';
import { NavBar } from './Components/NavBar/NavBar';
import { MyIFrame } from './Components/MyIFrame/MyIFrame';
import axios from 'axios';

const ReadArticle  = () => {
  
  // Gets article id
  const ID = window.location.toString().split('/')[4]
  const [articleData, setArticleData] = useState({})

  // Gets article data from backend
  axios({
    method: 'GET',
    url:'http://localhost:8081/article/',
    params: {ID: ID}
  }).then(res => {
    setArticleData(res.data[0])
  }).catch( err => {
    console.log(err)
  })  

  // Returns result
  return (
      <div>
        <section className="heading">
          <h1>NEWS PALATE</h1>
          <div className="navBar">
            {NavBar()}
          </div>
        </section>
        {MyIFrame(articleData.Link)}
        {/* <iframe id='myIFrameID' src={articleData.Link}></iframe> */}
      </div>
    );
}

export default ReadArticle;
