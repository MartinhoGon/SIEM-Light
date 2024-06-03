import {
  Card,
  CardHeader,
  CardBody,
  Typography,
} from "@material-tailwind/react";
import { useState, useEffect } from "react";
import { DataGrid } from '@mui/x-data-grid';
import axios from "axios";
import endpoints from '@/apiConfig';


export function Feeds() {
  const [feeds, setFeeds] = useState({
    feedRows: []
  })
  
  useEffect(() => {
    const fetchData = async () => {
            const response = await axios.get(endpoints.feeds).then(function (response) {
              setFeeds({
                    feedRows: response.data,
                });
              })
              .catch(function (error) {
                console.log(error)
                setShowAlerts({
                    active: true,
                    message: error.response ? error.response.data.message: error.message,
                    color: 'red'
                })
                console.error('Error fetching data:', error);
              });
            // const data = response.data;
      };

      fetchData();
  }, []);

  const columns = [
    { field: 'category', valueGetter: (value) => {
      return value.name;
    }, headerName: 'Category', width: 150 },
    { field: 'name', headerName: 'Name', width: 300 },
    { field: 'url', headerName: 'URL', width: 400 },
  ];
  return (
    <div className="mt-12 mb-8 flex flex-col gap-12">
      <Card>
        <CardHeader variant="gradient" color="gray" className="mb-8 p-6">
          <Typography variant="h6" color="white">
            Feeds
          </Typography>
        </CardHeader>
        <CardBody className="overflow-x-scroll px-0 pt-0 pb-2">
          <div style={{ padding: "0px 10px 0px 10px" }} className="w-full min-w-[640px] table-auto">
            <DataGrid rows={feeds["feedRows"]} columns={columns} />
          </div>
        </CardBody>
      </Card>
    </div>
  );
}

export default Feeds;
