import { Box } from "@mui/material";
import Header from "../../components/Header";
import LineChart from "../../components/LineChart";

const Line = () => {
  return (
    <Box m="20px">
<Header title="Freshness Analysis" subtitle="Freshness Percentage of Products Over the Last 6 Months" />
<Box height="75vh">
        <LineChart />
      </Box>
    </Box>
  );
};

export default Line;
