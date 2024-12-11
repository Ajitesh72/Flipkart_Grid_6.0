import { Box } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import Header from "../../components/Header";
import { useTheme } from "@mui/material";
import CircularProgress from '@mui/material/CircularProgress';
import { useEffect, useState } from "react";
import Button from '@mui/material/Button';
const ProductDetails = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [productDetails, setProductDetails] = useState(null);
  const [error, setError] = useState(false);
  const getAllProductDetails = async() => {
    setError(false);
    try {
      const response = await fetch("https://grid-flask-server.onrender.com/api/v1/get_product_details");
      if(response.ok){
        let data = await response.json();
        data = data.map(item => {
          return Object.fromEntries(
              Object.entries(item).map(([key, value]) => [key, value === null || value === "NULL" ? "N/A" : value])
          );
      });
        setProductDetails(data);
        
      }
      else{
        setError(true)
      }
    } 
    catch(error){
      console.log(error);
      setError(true)
    }
  }
  useEffect(() => {
    getAllProductDetails();
  }, [])
  const columns = [
    {
      field: "product_name",
      headerName: "Product",
      flex: 1,
      cellClassName: "name-column--cell",
      headerAlign: "left",
      align: "left",
    },
    {
      field: "product_category",
      headerName: "Category",
      flex: 1,
      headerAlign: "left",
      align: "left",
    },
    {
      field: "product_price",
      headerName: "Price",
      type: "number",
      flex: 1,
      headerAlign: "left",
      align: "left",
    },
    {
      field: "product_count",
      headerName: "Count",
      type: "number",
      flex: 1,
      headerAlign: "left",
      align: "left",
    },
    {
      field: "expiry_date",
      headerName: "Expiry",
      flex: 1,
      headerAlign: "left",
      align: "left",
    },
    {
      field: "estimated_shelf_life",
      headerName: "Est. Shelf Life",
      flex: 1,
      headerAlign: "left",
      align: "left",
    },
    {
      field: "city",
      headerName: "City",
      flex: 1,
      headerAlign: "left",
      align: "left",
    },
    {
      field: "zipcode",
      headerName: "Zip Code",
      flex: 1,
      headerAlign: "left",
      align: "left",
    },
  ];

  return (
    <Box m="20px">
      <Header title="Product Details" subtitle="List of scanned products" />
      {(productDetails && !error) ? <Box
        m="40px 0 0 0"
        height="75vh"
        sx={{
          "& .MuiDataGrid-root": {
            border: "none",
          },
          "& .MuiDataGrid-cell": {
            borderBottom: "none",
          },
          "& .name-column--cell": {
            color: colors.greenAccent[300],
          },
          "& .MuiDataGrid-columnHeaders": {
            backgroundColor: colors.blueAccent[700],
            borderBottom: "none",
          },
          "& .MuiDataGrid-virtualScroller": {
            backgroundColor: colors.primary[400],
          },
          "& .MuiDataGrid-footerContainer": {
            borderTop: "none",
            backgroundColor: colors.blueAccent[700],
          },
          "& .MuiCheckbox-root": {
            color: `${colors.greenAccent[200]} !important`,
          },
          "& .MuiDataGrid-toolbarContainer .MuiButton-text": {
            color: `${colors.grey[100]} !important`,
          },
        }}
      >
        <DataGrid
          rows={productDetails}
          columns={columns}
          components={{ Toolbar: GridToolbar }}
        />
      </Box>
      :(!error) ?
      (<Box sx={{ display: 'flex' }}>
        <CircularProgress style={{'color': colors.greenAccent[500]}} />
      </Box> ):
      (
        <Button variant="contained" color="error" style={{fontWeight: "bold"}}
        onClick={getAllProductDetails}
        >
          Error! Try Again
        </Button>
      )
      }
    </Box>
  );
};

export default ProductDetails;
