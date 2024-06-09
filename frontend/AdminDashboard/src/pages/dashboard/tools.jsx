import { useState, useEffect } from "react";
import axios from "axios";
import {
    Typography,
    Card,
    CardHeader,
    CardBody,
    Button,
    Switch,
    Alert,
    Radio,
    Input
  } from "@material-tailwind/react";
import endpoints from '@/apiConfig'; // Adjust the path as needed
import { DefaultDialog } from '@/widgets/layout/dialog';

export function Tools() {
    const [showAlerts, setShowAlerts] = useState({
        active: false,
        color: "green",
        message: "",
    });

    const [switchStates, setSwitchStates] = useState({
        is_listener_running: false,
        is_sniffer_running: false,
        is_using_rsyslog: false,
    });

    const [selectedFile, setSelectedFile] = useState(null);

    const [port, setPort] = useState("32000");

    const [interfaces, setInterfaces] = useState([]);
    const [sniffingInterface, setSniffingInterface] = useState(null);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const [open, setOpen] = useState(false);
    const [dialogMessage, setDialogMessage] = useState("This operation may take a while, please be patiant.");

    const handleOpen = () => setOpen(!open);

    useEffect(() => {
        fetchHelperData();
        fetchInterfaces();
    }, []);

    const fetchHelperData = async () => {
        const response = await axios.get(endpoints.getHelper).then(function (response) {
            setSwitchStates({
                is_listener_running: response.data.is_listener_running,
                is_sniffer_running: response.data.is_sniffer_running,
                is_using_rsyslog: response.data.is_using_rsyslog,
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


    const fetchInterfaces = async () => {
        const response = await axios.get(endpoints.getInterfaces).then(function (response) {
            setInterfaces(response.data.interfaces);
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

    const handleUpload = async () => {
        if (!selectedFile) {
            alert('Please select a file first!');
            return;
        }
        setOpen(true)
        const formData = new FormData();
        formData.append('file', selectedFile);

        const response = await axios.post(endpoints.fileUpload, formData, {
            headers: {
            'Content-Type': 'multipart/form-data',
            },
        }).then(function (response) {
            setOpen(false)
            setShowAlerts({
                active: true,
                message: response.data.message,
                color: 'green'
            })
          })
          .catch(function (error) {
            setOpen(false)
            setShowAlerts({
                active: true,
                message: error.response ? error.response.data.message: error.message,
                color: 'red'
            })
          });

       
    };

    const handleRequests = async (name, value, endpoint, data={}) => await axios.post(endpoint, 
        data)
        .then(function (response) {
            setShowAlerts({
                active: true,
                message: response.data.message,
                color: 'green'
            })
            setSwitchStates((prevState) => ({
                ...prevState,
                [name]: value
            }))
        })
        .catch(function (error) {
            console.log(error);
            setShowAlerts({
                active: true,
                message: error.response ? error.response.data.message: error.message,
                color: 'red'
            })
        });

    const onChangeSwitch = (event, name) => {
        event.target.checked
        
        if(event.target.checked == true){
            if(name === "is_listener_running"){
                handleRequests('is_listener_running', event.target.checked, endpoints.startListener, {
                    "port": port
                })
            }else if(name === "is_sniffer_running"){
                if(sniffingInterface === null){
                    setShowAlerts({
                        active: true,
                        message: "You must select a network interface first!",
                        color: 'red'
                    });
                    return
                }
                handleRequests('is_sniffer_running', event.target.checked, endpoints.startSniffer, {
                    "interface": sniffingInterface
                })
            }else if(name === "is_using_rsyslog"){

            }
        }else {
            if(name === "is_listener_running"){
                handleRequests('is_listener_running', event.target.checked, endpoints.stopListener)
            }else if(name === "is_sniffer_running"){
                handleRequests("is_sniffer_running", event.target.checked, endpoints.stopSniffer)
            }else if(name === "is_using_rsyslog"){
                
            }
        }
    }

    


    return(
        <div className="mt-12">
            <DefaultDialog 
                title={"Please wait"}
                open={open}
                message={dialogMessage}
                handleOpen={handleOpen}
                hideButtons={true}
            />
            <div className="mb-4 grid grid-cols-1 gap-6 xl:grid-cols-2">
                <Card className="border border-blue-gray-100 shadow-sm">
                    <CardHeader
                        floated={false}
                        shadow={false}
                        color="transparent"
                        className="m-0 p-6"
                    >
                        <Typography variant="h6" color="blue-gray" className="mb-2">
                        Actions
                        </Typography>
                    </CardHeader>
                    <CardBody className="pt-0">
                        <div className="flex flex-col gap-2">
                            <div className="flex flex-col gap-2">
                                <Switch
                                key={1}
                                id={1}
                                label={"Start/Stop Listener"}
                                checked={switchStates['is_listener_running']}
                                onChange={(event) => onChangeSwitch(event, 'is_listener_running')}
                                labelProps={{
                                    className: "text-sm font-normal text-blue-gray-500",
                                }}
                                />
                            </div>
                            <div className="flex flex-col gap-0">
                                <Typography variant="small" color="blue-gray" className="gap-2">
                                    Select a port for the listener
                                </Typography>
                                <div className="">
                                
                                    <Input className="" value={port} onChange={(event) => setPort(event.target.value)} />
                                </div>
                            </div>
                            <div className="flex flex-col gap-2">
                                <Switch
                                key={2}
                                id={2}
                                label={"Start/Stop Sniffer"}
                                checked={switchStates['is_sniffer_running']}
                                // onClick={()=>alert()}
                                onChange={(event) => onChangeSwitch(event, 'is_sniffer_running')}
                                labelProps={{
                                    className: "text-sm font-normal text-blue-gray-500",
                                }}
                                />
                            </div>
                            <div className="flex flex-col gap-0">
                                <Typography variant="small" color="blue-gray" className="gap-6">
                                    Select a sniffing interface
                                </Typography>
                                <div className="flex gap-5">
                                
                                    {interfaces.map((prop) => (
                                        <Radio key={prop} name="type" label={prop} onClick={() => setSniffingInterface(prop)} />
                                    ))}
                                </div>
                            </div>
                            <div className="flex flex-col gap-2">
                                <Switch
                                key={3}
                                id={3}
                                label={"Use rsyslog"}
                                checked={switchStates['is_using_rsyslog']}
                                onChange={(event) => onChangeSwitch(event,'is_using_rsyslog')}
                                labelProps={{
                                    className: "text-sm font-normal text-blue-gray-500",
                                }}
                                />
                            </div>
                            {/* <div className="flex flex-col gap-6">
                                <div className="flex flex-col gap-6">
                                <label
                                    htmlFor="formFile"
                                    className="mb-2 inline-block text-neutral-700 dark:text-neutral-200"
                                >
                                Upload file (.log/.pcap)
                                </label>
                                <input
                                    className="relative m-0 block w-full min-w-0 flex-auto rounded border border-solid border-neutral-300 bg-clip-padding px-3 py-[0.32rem] text-base font-normal text-neutral-700 transition duration-300 ease-in-out file:-mx-3 file:-my-[0.32rem] file:overflow-hidden file:rounded-none file:border-0 file:border-solid file:border-inherit file:bg-neutral-100 file:px-3 file:py-[0.32rem] file:text-neutral-700 file:transition file:duration-150 file:ease-in-out file:[border-inline-end-width:1px] file:[margin-inline-end:0.75rem] hover:file:bg-neutral-200 focus:border-primary focus:text-neutral-700 focus:shadow-te-primary focus:outline-none dark:border-neutral-600 dark:text-neutral-200 dark:file:bg-neutral-700 dark:file:text-neutral-100 dark:focus:border-primary"
                                    type="file"
                                id="formFile"
                                />
                                </div>
                                <div  className="flex flex-col gap-6">
                                    <Button variant="outlined" size="sm">
                                        Upload file
                                    </Button>
                                </div>
                            </div> */}
                        </div>
                    </CardBody>
                </Card>
            </div>
            <div className="mb-4 grid grid-cols-1 gap-6 xl:grid-cols-2">
                <Card className="border border-blue-gray-100 shadow-sm">
                    <CardHeader
                        floated={false}
                        shadow={false}
                        color="transparent"
                        className="m-0 p-6"
                    >
                        <Typography variant="h6" color="blue-gray" className="mb-2">
                        Files
                        </Typography>
                    </CardHeader>
                    <CardBody className="pt-0">
                        <div className="flex flex-col gap-2">
                            <div className="flex flex-col gap-2">
                                <div className="flex flex-col gap-2">
                                <label
                                    htmlFor="formFile"
                                    className="mb-2 inline-block text-neutral-700 dark:text-neutral-200"
                                >
                                Upload file - Only .log and .pcap files are allowed
                                </label>
                                <input
                                    className="relative m-0 block w-full min-w-0 flex-auto rounded border border-solid border-neutral-300 bg-clip-padding px-3 py-[0.32rem] text-base font-normal text-neutral-700 transition duration-300 ease-in-out file:-mx-3 file:-my-[0.32rem] file:overflow-hidden file:rounded-none file:border-0 file:border-solid file:border-inherit file:bg-neutral-100 file:px-3 file:py-[0.32rem] file:text-neutral-700 file:transition file:duration-150 file:ease-in-out file:[border-inline-end-width:1px] file:[margin-inline-end:0.75rem] hover:file:bg-neutral-200 focus:border-primary focus:text-neutral-700 focus:shadow-te-primary focus:outline-none dark:border-neutral-600 dark:text-neutral-200 dark:file:bg-neutral-700 dark:file:text-neutral-100 dark:focus:border-primary"
                                    type="file"
                                    id="formFile"
                                    onChange={handleFileChange}
                                />
                                </div>
                                <div  className="flex flex-col gap-2">
                                    <Button onClick={handleUpload} variant="outlined" size="sm">
                                        Upload file
                                    </Button>
                                </div>
                            </div>
                        </div>
                    </CardBody>
                </Card>
            </div>
            <Alert
              key={showAlerts['color']}
              open={showAlerts['active']}
              color={showAlerts['color']}
              onClose={() => setShowAlerts((current) => ({ ...current, color: "blue", active: false, message: "" }))}
            >
              {showAlerts['message']}
            </Alert>
        </div>
    )

}


export default Tools;