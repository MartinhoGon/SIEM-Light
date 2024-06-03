import {
  Card,
  CardHeader,
  CardBody,
  Typography,
  Button,
  Alert,
} from "@material-tailwind/react";
import {
  EyeIcon,
  EyeSlashIcon
} from "@heroicons/react/24/solid";
import { useState, useEffect, createElement } from "react";
import { DataGrid } from '@mui/x-data-grid';
import axios from "axios";
import endpoints from '@/apiConfig';
import { DefaultDialog } from '@/widgets/layout/dialog';

export function Alerts() {
  const [alerts, setAlerts] = useState({
    alertRows: []
  })

  const [showAlerts, setShowAlerts] = useState({
      active: false,
      color: "green",
      message: "Olá",
  });

  const [selectedRows, setSelectedRows] = useState([]);

  const [open, setOpen] = useState(false);
  const [dialogMessage, setDialogMessage] = useState("");
 
  const handleOpen = () => setOpen(!open);
  
  useEffect(() => {
      fetchAllAlerts();
  }, []);

  const fetchAllAlerts = async () => {
      const response = await axios.get(endpoints.alertEndpoint).then(function (response) {
        setAlerts({
              alertRows: response.data,
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
  const handleAck = async (id) => await axios.put(endpoints.alertEndpoint+id+"/")
    .then(function (response) {
        setShowAlerts({
            active: true,
            message: "This alert has been acknowledged successfully!",
            color: 'green'
        })
        fetchAllAlerts()
        // setSwitchStates((prevState) => ({
        //     ...prevState,
        //     [name]: value
        // }))
    })
    .catch(function (error) {
        console.log(error);
        setShowAlerts({
            active: true,
            message: error.response ? error.response.data.message: error.message,
            color: 'red'
        })
    });


  const columns = [
    { field: 'created_at', headerName: 'Created At', width: 110 },
    { field: 'level', headerName: 'Alert Level', width: 100 },
    { field: 'message', headerName: 'Message', width: 800 },
    { field: 'acknowledge', headerName: 'Acknowledge', width: 150, renderCell: (params) => (
      <strong>
        {params.value}
        <Button
          size="sm"
          color={ params.value ? 'green': 'red'}
          onClick={()=>{handleAck(params.id)}}
          style={{ marginLeft: 16 }}
          tabIndex={params.hasFocus ? 0 : -1}
        >
          {createElement(params.value ? EyeIcon : EyeSlashIcon, {
              className: "w-4 h-4 text-white",
            })}
        </Button>
      </strong> 
      ),
    },
  ];


  // const handleSelectionChange = (newSelection) => {
  //   console.log("new Selection",newSelection)
  //   setSelectedRows(newSelection);
    
  // };

  const handleRowDoubleClick = (params) => {
    // alert(`Row double-clicked: ${JSON.stringify(params.row, null, 2)}`);
    console.log(params.row.message)
    setDialogMessage(params.row.message)
    setOpen(!open)
  };

  return (
    <div className="mt-12 mb-8 flex flex-col gap-12">
      <Alert
        key={showAlerts['color']}
        open={showAlerts['active']}
        color={showAlerts['color']}
        onClose={() => setShowAlerts((current) => ({ ...current, color: "blue", active: false, message: "" }))}
      >
        {showAlerts['message']}
      </Alert>
      <DefaultDialog 
        title={"Alert Message"}
        open={open}
        message={dialogMessage}
        handleOpen={handleOpen}
      />
      <Card>
        <CardHeader variant="gradient" color="gray" className="mb-8 p-6">
          <Typography variant="h6" color="white">
            Alerts
          </Typography>
        </CardHeader>
        <CardBody className="overflow-x-scroll px-0 pt-0 pb-2">
          <div style={{ padding: "0px 10px 0px 10px", height: "100%" }} className="w-full min-w-[640px] table-auto">
            <DataGrid 
              rows={alerts["alertRows"]} 
              columns={columns} 
              initialState={{
                pagination: { paginationModel: { pageSize: 25 } },
              }}
              pageSizeOptions={[25, 50, 100]}
              // checkboxSelection
              onRowDoubleClick={handleRowDoubleClick}
              // onSelectionModelChange={handleSelectionChange}
            />
          </div>
        </CardBody>
      </Card>
    </div>
  );
}

export default Alerts;
