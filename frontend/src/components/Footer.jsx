import React from "react";
import "./Footer.css"; // Import CSS
import { Box, Container, Typography } from "@mui/material";

function Footer() {
  return (
    <Box className="footer">
      <Container maxWidth="lg">
        <Typography variant="subtitle1">
          {`${new Date().getFullYear()} | Built with React & Material UI`}
        </Typography>
      </Container>
    </Box>
  );
}

export default Footer;
