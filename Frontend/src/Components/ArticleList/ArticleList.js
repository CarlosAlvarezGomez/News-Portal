import React, { useState, useRef, useCallback } from 'react';
import './ArticleList.css';
import { Article } from '../Article/Article';
import { useGetArticles } from './useGetArticles';

export function ArticleList(category) {

  const [pageNumber, setPageNumber] = useState(1)

  const {loading, error, articles, hasMore} = useGetArticles(category, pageNumber)

  const observer = useRef()
  const lastArticleElementRef = useCallback(node =>
    {
      if (loading) {
        return
      }
      if (observer.current) {
        observer.current.disconnect()
      }
      observer.current = new IntersectionObserver( entries => {
        if (entries[0].isIntersecting && hasMore) {
          console.log("CHANGED PAGENUMBER")
          setPageNumber(prevPageNumber => prevPageNumber + 1)
        }
      })
      if (node) observer.current.observe(node)
    }, [loading, hasMore])

  return (
      <ul>
        <div className="row">
          <div className="column">
            {articles.map( (art, index) => {
              if (articles.length === index + 1){
                return (<div ref={lastArticleElementRef}>{Article(art)}</div>);
              } 
              else {
                return Article(art);
              }
              }
            )
            }

          </div>
          <div className="column">
            {articles.map( (art, index) => {
              return Article(art)})}
          </div>
        </div>
      </ul>
    )
  }