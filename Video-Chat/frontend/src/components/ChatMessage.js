import React from 'react';

const ChatMessage = ({ message, role, timestamps = [], onTimestampClick }) => {
  // Function to parse the message and add clickable timestamps
  const parseMessage = () => {
    if (!message) return '';

    // Pattern for [MM:SS] format
    const pattern1 = /\[(\d{1,2}):(\d{2})\]/g;
    // Pattern for [HH:MM:SS] format
    const pattern2 = /\[(\d{1,2}):(\d{2}):(\d{2})\]/g;
    // Pattern for timestamps like [12.34 → 45.67]
    const pattern3 = /\[(\d+\.\d+)\s*(?:→|-|to)\s*(\d+\.\d+)\]/g;

    // Replace timestamps with clickable spans
    let formattedMessage = message;

    // Replace [MM:SS] timestamps
    formattedMessage = formattedMessage.replace(pattern1, (match, minutes, seconds) => {
      const timeInSeconds = parseInt(minutes) * 60 + parseInt(seconds);
      return `<span class="timestamp-link" data-time="${timeInSeconds}">${match}</span>`;
    });

    // Replace [HH:MM:SS] timestamps
    formattedMessage = formattedMessage.replace(pattern2, (match, hours, minutes, seconds) => {
      const timeInSeconds = parseInt(hours) * 3600 + parseInt(minutes) * 60 + parseInt(seconds);
      return `<span class="timestamp-link" data-time="${timeInSeconds}">${match}</span>`;
    });

    // Replace [start → end] timestamps
    formattedMessage = formattedMessage.replace(pattern3, (match, start, end) => {
      return `<span class="timestamp-link" data-time="${start}">${match}</span>`;
    });

    return formattedMessage;
  };

  // Handle click on timestamp
  const handleClick = (e) => {
    if (e.target.classList.contains('timestamp-link') && onTimestampClick) {
      const time = parseFloat(e.target.getAttribute('data-time'));
      onTimestampClick(time);
    }
  };

  return (
    <div 
      className={`chat-message ${role === 'user' ? 'user-message' : 'assistant-message'}`}
      onClick={handleClick}
      dangerouslySetInnerHTML={{ __html: parseMessage() }}
    />
  );
};

export default ChatMessage; 