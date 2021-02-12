import { useEffect, useState } from 'react';
import axios from 'axios';

export function useGetArticles(category, pageNumber) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [articles, setArticles] = useState([]);
  const [hasMore, setHasMore] = useState(false);

  // This funciton is used whenever pageNumber changes
  useEffect(
    () =>  {
      setLoading(true);
      setError(false);

      // Requst next page of articles from api and append it to current list of
      // articles
      axios({
        method: 'GET',
        url:'http://localhost:8081/articles/',
        params: {category: category, requestNumber: pageNumber}
      }).then(res => {

        // Appends the new articles to the end of the current article list
        setArticles([... articles, ...res.data])
      }).catch( err => {
        setError(true)
      })

      setHasMore(true);
      setLoading(false);
  }, [pageNumber])

  return { loading, error, articles, hasMore };
}