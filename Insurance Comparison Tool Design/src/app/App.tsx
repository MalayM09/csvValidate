import React from 'react';
import { RouterProvider } from 'react-router';
import { router } from './routes';
import '../styles/theme.css'; // Make sure global styles are loaded

export default function App() {
  return (
    <div className="font-['Inter'] min-h-screen text-[#212529] bg-white">
      <RouterProvider router={router} />
    </div>
  );
}
