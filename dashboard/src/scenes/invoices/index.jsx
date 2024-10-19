import { Box, Typography, useTheme } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import { mockDataInvoices } from "../../data/mockData";
import Header from "../../components/Header";

const Invoices = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const columns = [
    { field: "id", headerName: "Scanner Id" },
    {
      field: "name",
      headerName: "Registrar Id",
      flex: 1,
      cellClassName: "name-column--cell",
    },
    {
      field: "phone",
      headerName: "Product Name",
      flex: 1,
    },
    {
      field: "email",
      headerName: "Quantity",
      flex: 1,
    },
    {
      field: "cost",
      headerName: "Cost",
      flex: 1,
      renderCell: (params) => (
        <Typography color={colors.greenAccent[500]}>
          INR {params.row.cost}
        </Typography>
      ),
    },
    {
      field: "date",
      headerName: "Expiry Date",
      flex: 1,
    },
    {
      field: "freshness",
      headerName: "Freshness",  //it could be high,medium,low
      flex: 1,
    },
    {
      field: "remarks",
      headerName: "Remarks(While scanning)",  //it could be anything which the scanner person wrote:a very short line or N/A
      flex: 1,
    },
  ];

  return (
    <Box m="20px">
      <Header title="SCANNER DETAILS" subtitle="List of Scanned Items" />
      <Box
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
            color: `INR {colors.greenAccent[200]} !important`,
          },
        }}
      >
        <DataGrid checkboxSelection rows={mockDataInvoices} columns={columns} />
      </Box>
    </Box>
  );
};

export default Invoices;
