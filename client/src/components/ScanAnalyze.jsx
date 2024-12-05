import React, { useState, useEffect, useRef } from "react";
import {
  Button,
  Typography,
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import CircularProgress from "@mui/material/CircularProgress";
import { Upload, Camera } from "lucide-react";

const freshnessData = [
  {
    id: 1,
    product_name: "apple",
    freshness: "good",
    count: "1",
    remark: "It is a fresh apple",
  },
  {
    id: 2,
    product_name: "banana",
    freshness: "poor",
    count: "3",
    remark: "It is not fresh",
  },
];

const productDetailsData = [
  {
    id: 1,
    product: "CORN FLAKES",
    count: 1,
    price: 20,
    expiry_date: "9 Months",
  },
  {
    id: 2,
    product: "Waffers",
    count: 29,
    remark: "Various snacks like Lay's and Kurkure are visible.",
  },
];

const getLocation = () =>
  new Promise((resolve, reject) => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          resolve({ latitude, longitude });
        },
        (error) => reject(error)
      );
    } else {
      reject(new Error("Geolocation is not supported by this browser."));
    }
  });

const ScanAnalyze = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [image, setImage] = useState(null);
  const [freshnessIndex, setFreshnessIndex] = useState(0);
  const [detailsIndex, setDetailsIndex] = useState(0);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  var user = "";
  var user = localStorage.getItem("user");

  useEffect(() => {
    const signedIn = localStorage.getItem("signedIn");
    if (signedIn !== "true") {
      window.location.href = "/signin";
    }
  }, []);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => setImage(e.target.result);
      reader.readAsDataURL(file);
      setResult(null);
    }
  };

  const handleCameraCapture = async () => {
    if (videoRef.current) {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
      videoRef.current.play();
      setResult(null);
    }
  };

  const captureImage = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageUrl = canvas.toDataURL();
    setImage(imageUrl);

    const stream = video.srcObject;
    const tracks = stream.getTracks();
    tracks.forEach((track) => track.stop());
    video.srcObject = null;
    setResult(null);
  };

  const handleAnalyzeFreshness = async () => {
    console.log("kuch");
    if (!image) {
      alert("Please upload or capture an image first.");
      return;
    }
    setLoading(true);

    try {
      const location = await getLocation();
      console.log(location);
      
      const response = await fetch(
        "http://localhost:8000/api/v1/analyze_product_details",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json", // Setting the content type to JSON
          },
          body: JSON.stringify({
            image: image,
            location: location, // Send the base64 image string
          }),
        }
      );
      const data = await response.json();
      if (response.ok) {
        console.log(data);
        setResult(data);


        // alert(data); // Display the message from Flask
      } else {
        alert("Error: " + data.error || "Something went wrong");
      }
      // console.log()
      setLoading(false);
    } catch (error) {
      setLoading(false);
    }
  };

  const handleAnalyzeDetails = async () => {
    if (!image) {
      alert("Please upload or capture an image first.");
      return;
    }
    setLoading(true);

    try {
      const location = await getLocation();

      const response = await fetch(
        "http://localhost:8000/api/v1/analyze_product_details",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json", // Setting the content type to JSON
          },
          body: JSON.stringify({
            image: image,
            location: location, // Send the base64 image string
          }),
        }
      );
      const data = await response.json();
      if (response.ok) {
        console.log(data);
        setResult(data);
        // alert(data.message); // Display the message from Flask
      } else {
        alert("Error: " + data.error || "Something went wrong");
      }
      setLoading(false);
    } catch (error) {
      setLoading(false);
    }

    
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "background.default",
        padding: 3,
      }}
    >
      <Typography
        variant="h4"
        color="text.primary"
        sx={{ textAlign: "center" }}
        gutterBottom
      >
        Hey {user} !! Welcome Back
      </Typography>
      <Typography
        variant="h4"
        color="text.primary"
        sx={{ textAlign: "center" }}
        gutterBottom
      >
        Scan and Analyze Product
      </Typography>

      <Paper
        elevation={3}
        sx={{
          p: 3,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 2,
          maxWidth: 400,
          width: "100%",
        }}
      >
        <Typography variant="h6" color="text.secondary">
          Upload your product image
        </Typography>

        <Box sx={{ display: "flex", gap: 2 }}>
          <Button variant="contained" component="label" startIcon={<Upload />}>
            Upload File
            <input
              type="file"
              hidden
              onChange={handleFileUpload}
              accept="image/*"
            />
          </Button>

          <Button
            variant="contained"
            onClick={handleCameraCapture}
            startIcon={<Camera />}
          >
            Camera
          </Button>
        </Box>

        <Button variant="contained" sx={{ mt: 2 }} onClick={captureImage}>
          Capture Image
        </Button>

        {!image && (
          <>
            <video
              ref={videoRef}
              style={{ width: "100%", maxHeight: 400, objectFit: "cover" }}
            />
            <canvas ref={canvasRef} style={{ display: "none" }} />
          </>
        )}

        {image && (
          <Box
            sx={{
              mt: 2,
              width: "100%",
              aspectRatio: "4/3",
              position: "relative",
            }}
          >
            <img
              src={image}
              alt="Uploaded product"
              style={{ width: "100%", height: "100%", objectFit: "cover" }}
            />
          </Box>
        )}
      </Paper>

      <Box sx={{ mt: 3, display: "flex", gap: 2 }}>
        <Button
          variant="contained"
          color="secondary"
          onClick={handleAnalyzeFreshness}
          disabled={!image || loading}
        >
          Analyze Freshness
        </Button>

        <Button
          variant="contained"
          color="secondary"
          onClick={handleAnalyzeDetails}
          disabled={!image || loading}
        >
          Analyze Product Details
        </Button>
      </Box>

      {loading && <CircularProgress sx={{ mt: 2 }} />}

      {result && (
        <TableContainer component={Paper} sx={{ mt: 2 }}>
          <Table>
            <TableHead>
              <TableRow>
                {/* <TableCell>ID</TableCell> */}
                <TableCell>Product Name</TableCell>
                <TableCell>Product Category</TableCell>
                <TableCell>Price</TableCell>
                <TableCell>Count</TableCell>
                <TableCell>Expiry Date</TableCell>
                <TableCell>Estimated Shelf Life</TableCell>
                {/* <TableCell>Freshness</TableCell> */}
                {/* <TableCell>Remark</TableCell> */}
              </TableRow>
            </TableHead>
            <TableBody>
              {result.map((item, index) => (
                <TableRow key={index}>
                  <TableCell>{item.product_name === "NULL" ?"-":item.product_name|| "-"}</TableCell>
                  <TableCell>{item.product_category==="NULL"?"-":item.product_category || "-"}</TableCell>
                  <TableCell>{item.product_price === "NULL"?"-":item.product_price || "-"}</TableCell>
                  <TableCell>{item.product_count || "-"}</TableCell>
                  <TableCell>{item.expiry_date==="NULL"?"-":item.expiry_date || "-"}</TableCell>
                  <TableCell>{item.estimated_shelf_life==="NULL"?"-":item.estimated_shelf_life || "-"}</TableCell>
                </TableRow>
              ))}
              {/* <TableRow>
                <TableCell>{result.id || '-'}</TableCell>
                <TableCell>{result.product_name || result.product || '-'}</TableCell>
                <TableCell>{result.price || '-'}</TableCell>
                <TableCell>{result.price || '-'}</TableCell>
                <TableCell>{result.count || '-'}</TableCell>
                <TableCell>{result.expiry_date || '-'}</TableCell>
                <TableCell>{result.freshness || '-'}</TableCell>
                <TableCell>{result.remark || '-'}</TableCell>
              </TableRow> */}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
};

export default ScanAnalyze;
