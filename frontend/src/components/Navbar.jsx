import React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import './Navbar.css'; 

function Navbar() {
  return (
    <Box className="navbar-container">
      <AppBar position="static" className="navbar">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            className="menu-icon"
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" className="navbar-title">
            Best Price IT
          </Typography>
          <Button color="inherit" className="login-button">
            Login
          </Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}

export default Navbar;
