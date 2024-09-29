import React, { useState } from "react";
import {
    Typography,
    Container,
    Grid,
    Card,
    CardContent,
    Button,
    AppBar,
    Toolbar,
    IconButton,
    Drawer,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    Divider,
    CssBaseline,
} from "@mui/material";
import {
    Upload as UploadIcon,
    Menu as MenuIcon,
    Home as HomeIcon,
    Info as InfoIcon,
} from "@mui/icons-material";
import axios from "axios";
import { motion } from "framer-motion";
import { ClipLoader } from "react-spinners";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";

const drawerWidth = 240;

function UploadPage() {
    const [mobileOpen, setMobileOpen] = useState(false);

    const handleDrawerToggle = () => {
        setMobileOpen(!mobileOpen);
    };

    const drawer = (
        <div>
            <Toolbar />
            <Divider />
            <List>
                {["Home", "Upload", "About"].map((text, index) => (
                    <ListItem
                        button
                        key={text}
                        component={Link}
                        to={`/${text.toLowerCase()}`}
                    >
                        <ListItemIcon>
                            {index === 0 ? (
                                <HomeIcon />
                            ) : index === 1 ? (
                                <UploadIcon />
                            ) : (
                                <InfoIcon />
                            )}
                        </ListItemIcon>
                        <ListItemText primary={text} />
                    </ListItem>
                ))}
            </List>
        </div>
    );

    return (
        <Router>
            <div style={{ display: "flex" }}>
                <CssBaseline />
                <AppBar
                    position="fixed"
                    style={{ zIndex: 1201 }} // Ensure AppBar is above the Drawer
                >
                    <Toolbar>
                        <IconButton
                            color="inherit"
                            aria-label="open drawer"
                            edge="start"
                            onClick={handleDrawerToggle}
                            style={{ marginRight: "20px" }}
                        >
                            <MenuIcon />
                        </IconButton>
                        <Typography variant="h6" noWrap>
                            Image Prediction App
                        </Typography>
                    </Toolbar>
                </AppBar>
                <nav
                    style={{ width: drawerWidth, flexShrink: 0 }}
                    aria-label="mailbox folders"
                >
                    <Drawer
                        variant="temporary"
                        open={mobileOpen}
                        onClose={handleDrawerToggle}
                        ModalProps={{
                            keepMounted: true, // Better open performance on mobile.
                        }}
                        sx={{
                            display: { xs: "block", sm: "none" },
                            "& .MuiDrawer-paper": {
                                boxSizing: "border-box",
                                width: drawerWidth,
                            },
                        }}
                    >
                        {drawer}
                    </Drawer>
                    <Drawer
                        variant="permanent"
                        sx={{
                            display: { xs: "none", sm: "block" },
                            "& .MuiDrawer-paper": {
                                boxSizing: "border-box",
                                width: drawerWidth,
                            },
                        }}
                        open
                    >
                        {drawer}
                    </Drawer>
                </nav>
                <main style={{ flexGrow: 1, padding: "80px 24px 24px 24px" }}>
                    <Container>
                        <Routes>
                            <Route path="/home" element={<HomePage />} />
                            <Route path="/upload" element={<UploadForm />} />
                            <Route path="/about" element={<AboutPage />} />
                        </Routes>
                    </Container>
                </main>
            </div>
        </Router>
    );
}

function HomePage() {
    return (
        <Container>
            <Typography variant="h4" align="center" gutterBottom>
                Welcome to the Image Prediction App
            </Typography>
        </Container>
    );
}

function AboutPage() {
    return (
        <Container>
            <Typography variant="h4" align="center" gutterBottom>
                About This Application
            </Typography>
            <Typography align="center">
                This app allows you to upload images for AI-based cancer
                detection.
            </Typography>
        </Container>
    );
}

function UploadForm() {
    const [file, setFile] = useState(null);
    const [prediction, setPrediction] = useState(null);
    const [confidence, setConfidence] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        setFile(selectedFile);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) {
            setError("Please select a file.");
            return;
        }

        const formData = new FormData();
        formData.append("image", file);

        setLoading(true);
        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/upload/", // Django backend URL
                formData,
                {
                    headers: { "Content-Type": "multipart/form-data" },
                }
            );
            setPrediction(
                response.data.is_cancerous ? "Cancerous" : "Not Cancerous"
            );
            setConfidence(response.data.confidence);
            setError(null);
        } catch (error) {
            setError("Error during prediction. Please try again.");
            setPrediction(null);
            setConfidence(null);
        }
        setLoading(false);
    };

    return (
        <Grid container spacing={4} justifyContent="center">
            <Grid item xs={12} md={8}>
                <Card elevation={3}>
                    <CardContent>
                        <Typography variant="h4" gutterBottom align="center">
                            Upload Image for Prediction
                        </Typography>
                        <form
                            onSubmit={handleSubmit}
                            encType="multipart/form-data"
                        >
                            <Grid container spacing={2}>
                                <Grid item xs={12}>
                                    <input
                                        accept="image/*"
                                        style={{ display: "none" }}
                                        id="upload-file"
                                        type="file"
                                        onChange={handleFileChange}
                                    />
                                    <label htmlFor="upload-file">
                                        <Button
                                            variant="contained"
                                            component="span"
                                            fullWidth
                                            startIcon={<UploadIcon />}
                                        >
                                            Choose Image
                                        </Button>
                                    </label>
                                </Grid>
                                <Grid item xs={12}>
                                    <motion.div whileHover={{ scale: 1.02 }}>
                                        <Button
                                            variant="contained"
                                            color="primary"
                                            type="submit"
                                            fullWidth
                                            startIcon={<UploadIcon />}
                                        >
                                            Upload and Predict
                                        </Button>
                                    </motion.div>
                                </Grid>
                            </Grid>
                        </form>
                        {loading && (
                            <Grid
                                container
                                justifyContent="center"
                                style={{ marginTop: "20px" }}
                            >
                                <ClipLoader
                                    color="#3f51b5"
                                    loading={loading}
                                    size={50}
                                />
                            </Grid>
                        )}
                        {error && (
                            <Typography
                                variant="h6"
                                color="error"
                                align="center"
                                style={{ marginTop: "20px" }}
                            >
                                {error}
                            </Typography>
                        )}
                        {prediction && (
                            <div style={{ marginTop: "20px" }}>
                                <Typography
                                    variant="h6"
                                    color="textPrimary"
                                    align="center"
                                >
                                    Prediction: {prediction}
                                </Typography>
                                {confidence && (
                                    <Typography
                                        variant="subtitle1"
                                        color="textSecondary"
                                        align="center"
                                    >
                                        Confidence:{" "}
                                        {(confidence * 100).toFixed(2)}%
                                    </Typography>
                                )}
                            </div>
                        )}
                    </CardContent>
                </Card>
            </Grid>
        </Grid>
    );
}

export default UploadPage;
