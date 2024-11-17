import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { fetchYouTubeData} from '../api/youtubeApi'

const API_BASE = 'http://localhost:8000/youtube/';

const FetchDataForm = () => {
  const [channelUrl, setChannelUrl] = useState(''); // For YouTube channel URL input
  const [comments, setComments] = useState([]); // For storing fetched comments
  const [error, setError] = useState(null); // For error handling
  const [loading, setLoading] = useState(false);


  const handleFetch = async () => {
    if (!channelUrl) {
      alert('Please enter a YouTube channel URL.');
      return;
    }

    setLoading(true);
    try {
      await fetchYouTubeData(channelUrl);
      alert('Data fetched successfully!');
    } catch (err) {
      alert('Error fetching data.');
    } finally {
      setLoading(false);
    }
  };

  // Function to fetch comments from the backend
  const fetchComments = async () => {
    try {
      const response = await axios.get(`${API_BASE}comments/`);
      if (response.status === 200) {
        setComments(response.data);
      } else {
        throw new Error('Failed to fetch comments.');
      }
    } catch (err) {
      console.error('Error fetching comments:', err);
      setError('Error fetching comments.');
    }
  };

  // Function to download all comments as an Excel file
  const handleDownloadExcel = async () => {
    try {
      const response = await axios.get(`${API_BASE}export-comments/`, {
        responseType: 'blob', // Ensure the response is treated as a binary file
      });
  
      const blob = new Blob([response.data], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      });
  
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'comments.xlsx');
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (err) {
      console.error('Error downloading the Excel file:', err);
      alert('Failed to download the Excel file. Please try again.');
    }
  };
  

  useEffect(() => {
    fetchComments(); // Fetch comments on component mount
  }, []);

  return (
    <div>
      <h2>YouTube Comments Fetcher</h2>

      {/* Input for YouTube Channel URL */}
      <input
        type="text"
        placeholder="Enter YouTube Channel URL"
        value={channelUrl}
        onChange={(e) => setChannelUrl(e.target.value)}
      />
      <button onClick={handleFetch} disabled={loading}>
          {loading ? 'Fetching...' : 'Fetch Data'}
        </button>

      {/* Comments Table */}
      <table border="1">
        <thead>
          <tr>
            <th>Comment ID</th>
            <th>Comment Text</th>
            <th>Author</th>
          </tr>
        </thead>
        <tbody>
          {comments.length > 0 ? (
            comments.map((comment) => (
              <tr key={comment.comment_id}>
                <td>{comment.comment_id}</td>
                <td>{comment.text}</td>
                <td>{comment.author}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="3">No comments available</td>
            </tr>
          )}
        </tbody>
      </table>

      {/* Button to download comments as Excel */}
      <button onClick={handleDownloadExcel}>Download Excel</button>
    </div>
  );
};

export default FetchDataForm;
