import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { fetchYouTubeData} from '../api/youtubeApi'
import {
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Button,
  TextField,
  CircularProgress,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const API_BASE = 'http://localhost:8000/youtube/';

const FetchDataForm = () => {
  const [channelUrl, setChannelUrl] = useState('');
  const [videoData, setVideoData] = useState([]); // For storing video data
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // insert data into backend
  const submitUrl = async () => {
    if (!channelUrl) {
      alert('Please enter a YouTube channel URL.');
      return;
    }
  
    setLoading(true);
    try {
      const response = await fetchYouTubeData(channelUrl);
      console.log(response);
  
      if (response.status === 200) {
        alert('Data fetched successfully!');
        window.location.reload(); // Refresh the page
      } else {
        alert('Data fetched, but there was an issue.');
      }
    } catch (err) {
      console.error('Error:', err);
      alert('Error fetching data.');
    } finally {
      setLoading(false);
    }
  };
  

  const fetchVideos = async () => {
    try {
      const response = await axios.get(`${API_BASE}comments/`);
      if (response.status === 200) {
        setVideoData(response.data);
      } else {
        throw new Error('Failed to fetch video data.');
      }
    } catch (err) {
      console.error('Error fetching video data:', err);
      setError('Error fetching video data.');
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
    fetchVideos();
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        YouTube Video and Comments Viewer
      </Typography>

      {/* Input for Channel URL */}
       {/* Input for Channel URL */}
       <Box sx={{ mb: 2, display: 'flex', gap: 2 }}>
        <TextField
          label="YouTube Channel URL"
          variant="outlined"
          fullWidth
          value={channelUrl}
          onChange={(e) => setChannelUrl(e.target.value)}
        />
        <Button
          variant="contained"
          color="primary"
          onClick={submitUrl}
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} /> : 'Submit YouTube Url'}
        </Button>
      </Box>

      {/* Video Data and Comments */}
      {videoData.map((video) => (
        <Accordion key={video.video_id} sx={{ mb: 2 }}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography>
              {video.title} ({video.view_count} views, {video.like_count} likes)
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography sx={{ mb: 2 }}>
              <strong>Description:</strong> {video.description}
            </Typography>
            <Typography sx={{ mb: 2 }}>
              <strong>Total Comments:</strong> {video.comment_count}
            </Typography>

            <Typography variant="h6">Comments:</Typography>
            <TableContainer component={Paper} sx={{ mb: 3 }}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Comment ID</TableCell>
                    <TableCell>Text</TableCell>
                    <TableCell>Published Date</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {video.comments.length > 0 ? (
                    video.comments.map((comment) => (
                      <TableRow key={comment.comment_id}>
                        <TableCell>{comment.comment_id}</TableCell>
                        <TableCell>
                          <div
                            dangerouslySetInnerHTML={{
                              __html: comment.text,
                            }}
                          />
                        </TableCell>
                        <TableCell>
                          {new Date(comment.published_date).toLocaleString()}
                        </TableCell>
                      </TableRow>
                    ))
                  ) : (
                    <TableRow>
                      <TableCell colSpan={3}>No comments available</TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </AccordionDetails>
        </Accordion>
      ))}

      {/* Button to Download Excel */}
      <Button
        variant="contained"
        color="secondary"
        onClick={handleDownloadExcel}
      >
        Download Comments as Excel
      </Button>
    </Box>
  );
};

export default FetchDataForm;
