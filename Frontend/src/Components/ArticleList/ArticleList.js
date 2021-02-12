import React, { useState, useRef, useCallback } from 'react';
import './ArticleList.css';
import { Article } from '../Article/Article';
import { useGetArticles } from './useGetArticles';

export function ArticleList(category) {

  // Creates pageNumber variable
  const [pageNumber, setPageNumber] = useState(1)

  // Gets loading, error, and hasMore state variables to inform frontend about
  // the state of the backend. Also gets a list of articles to be presented
  const {loading, error, articles, hasMore} = useGetArticles(category, pageNumber)

  // Creates an observer which increases the pageNumber each time it appears on
  // screen
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
          setPageNumber(prevPageNumber => prevPageNumber + 1)
        }
      })
      if (node) observer.current.observe(node)
    }, [loading, hasMore])

  // Returns two columns: a left on and then a right one. Then it fills both
  // columns up with articles
  return (
      <ul>
          <div className="column">
            {articles.map( (art, index) => {
              // Adds the observer if this is the second to last article of the
              // list 
              if (articles.length === index + 2) {
                return (<div ref={lastArticleElementRef}>{Article(art, index, 'left')}</div>);

              } else {
                return Article(art, index, 'left');
              }
            })}

          </div>
          <div className="column">
            {articles.map( (art, index) => {
              // Adds the observer if this is the second to last article of the
              // list 
              if (articles.length === index + 2) {
                return (<div ref={lastArticleElementRef}>{Article(art, index, 'right')}</div>);
                
              } else {
                return Article(art, index, 'right');
              }
            })}
          </div>
      </ul>
    )
  }