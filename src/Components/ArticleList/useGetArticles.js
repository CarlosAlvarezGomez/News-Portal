import React, { useEffect, useState } from 'react';
import { Article } from "../Article/Article";

export function useGetArticles(category, pageNumber) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [articles, setArticles] = useState([]);
  const [hasMore, setHasMore] = useState(false);

  useEffect(() => {
    setLoading(true);
    setError(false);
    setArticles(prevArticles => {
      return [...prevArticles, < Article image={category} />]
    });
    setHasMore(true);
    setLoading(false);
  }, [category, pageNumber])
  return { loading, error, articles, hasMore };
}