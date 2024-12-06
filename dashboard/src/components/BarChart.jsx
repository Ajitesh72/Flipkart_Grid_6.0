import { useTheme } from "@mui/material";
import { ResponsiveBar } from "@nivo/bar";
import { useState, useEffect } from "react";
import { tokens } from "../theme";
import { mockBarData as data } from "../data/mockData";

const BarChart = ({ isDashboard = false }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [data, setData] = useState([]); 
  const [keys, setKeys] = useState([]);
    useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/v1/get_product_details");
        const products = await response.json();

        // Initialize an object to hold product counts by city and category
        const cityCategoryData = {};

        products.forEach((product) => {
          const { city, product_category, product_count } = product;

          // Make sure the product count is an integer
          const count = parseInt(product_count) || 0;

          // If city does not exist, initialize it
          if (!cityCategoryData[city]) {
            cityCategoryData[city] = {};
          }

          // If category does not exist for this city, initialize it
          if (!cityCategoryData[city][product_category]) {
            cityCategoryData[city][product_category] = 0;
          }

          // Add the count to the category for this city
          cityCategoryData[city][product_category] += count;
        });

        // Transform the data to the format expected by the bar chart
        const formattedData = Object.keys(cityCategoryData).map((city) => {
          const cityInfo = { city: city };

          // Add product category counts to the city object
          Object.keys(cityCategoryData[city]).forEach((category) => {
            cityInfo[category] = cityCategoryData[city][category];
          });

          return cityInfo;
        });

        setData(formattedData);

        // Calculate the total count per category across all cities
        const categoryCounts = {};
        products.forEach((product) => {
          const { product_category, product_count } = product;
          const count = parseInt(product_count) || 0;

          if (!categoryCounts[product_category]) {
            categoryCounts[product_category] = 0;
          }

          categoryCounts[product_category] += count;
        });

        // Get the top 7 categories based on the total count
        const topCategories = Object.keys(categoryCounts)
          .sort((a, b) => categoryCounts[b] - categoryCounts[a]) // Sort by descending total count
          .slice(0, 7); // Get top 7

        setKeys(topCategories);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  // useEffect(() => {
  //   const fetchData = async () => {
  //     try {
  //       const response = await fetch("http://localhost:8000/api/v1/get_product_details");
  //       const products = await response.json();

  //       // Initialize an object to hold product counts by city and category
  //       const cityCategoryData = {};

  //       products.forEach((product) => {
  //         const { city, product_category, product_count } = product;

  //         // Make sure the product count is an integer
  //         const count = parseInt(product_count) || 0;

  //         // If city does not exist, initialize it
  //         if (!cityCategoryData[city]) {
  //           cityCategoryData[city] = {};
  //         }

  //         // If category does not exist for this city, initialize it
  //         if (!cityCategoryData[city][product_category]) {
  //           cityCategoryData[city][product_category] = 0;
  //         }

  //         // Add the count to the category for this city
  //         cityCategoryData[city][product_category] += count;
  //       });

  //       // Transform the data to the format expected by the bar chart
  //       const formattedData = Object.keys(cityCategoryData).map((city) => {
  //         const cityInfo = { city: city };

  //         // Add product category counts to the city object
  //         Object.keys(cityCategoryData[city]).forEach((category) => {
  //           cityInfo[category] = cityCategoryData[city][category];
  //         });

  //         return cityInfo;
  //       });

  //       setData(formattedData);
  //     } catch (error) {
  //       console.error("Error fetching data:", error);
  //     }
  //   };

  //   fetchData();
  // }, []);
  console.log(data)
  console.log(keys)


  return (
<ResponsiveBar
  data={data}
  theme={{
    // added
    axis: {
      domain: {
        line: {
          stroke: colors.grey[100],
        },
      },
      legend: {
        text: {
          fill: colors.grey[100],
        },
      },
      ticks: {
        line: {
          stroke: colors.grey[100],
          strokeWidth: 1,
        },
        text: {
          fill: colors.grey[100],
        },
      },
    },
    legends: {
      text: {
        fill: colors.grey[100],
      },
    },
  }}
  // Update the keys here
  // keys={["Sauce", "Fruit", "Ghee", "Instant Noodles", "Oil", "Salt"]}
  keys={keys}
  indexBy="city"
  margin={{ top: 50, right: 130, bottom: 50, left: 60 }}
  padding={0.3}
  valueScale={{ type: "linear" }}
  indexScale={{ type: "band", round: true }}
  colors={{ scheme: "nivo" }}
  defs={[
    {
      id: "dots",
      type: "patternDots",
      background: "inherit",
      color: "#38bcb2",
      size: 4,
      padding: 1,
      stagger: true,
    },
    {
      id: "lines",
      type: "patternLines",
      background: "inherit",
      color: "#eed312",
      rotation: -45,
      lineWidth: 6,
      spacing: 10,
    },
  ]}
  borderColor={{
    from: "color",
    modifiers: [["darker", "1.6"]],
  }}
  axisTop={null}
  axisRight={null}
  axisBottom={{
    tickSize: 5,
    tickPadding: 5,
    tickRotation: 0,
    legend: isDashboard ? undefined : "State", // Updated legend
    legendPosition: "middle",
    legendOffset: 32,
  }}
  axisLeft={{
    tickSize: 5,
    tickPadding: 5,
    tickRotation: 0,
    legend: isDashboard ? undefined : "Categories", // Updated legend
    legendPosition: "middle",
    legendOffset: -40,
  }}
  enableLabel={false}
  labelSkipWidth={12}
  labelSkipHeight={12}
  labelTextColor={{
    from: "color",
    modifiers: [["darker", 1.6]],
  }}
  legends={[
    {
      dataFrom: "keys",
      anchor: "bottom-right",
      direction: "column",
      justify: false,
      translateX: 120,
      translateY: 0,
      itemsSpacing: 2,
      itemWidth: 100,
      itemHeight: 20,
      itemDirection: "left-to-right",
      itemOpacity: 0.85,
      symbolSize: 20,
      effects: [
        {
          on: "hover",
          style: {
            itemOpacity: 1,
          },
        },
      ],
    },
  ]}
  role="application"
  barAriaLabel={function (e) {
    return e.id + ": " + e.formattedValue + " in state: " + e.indexValue; // Updated for clarity
  }}
/>

  );
};

export default BarChart;
