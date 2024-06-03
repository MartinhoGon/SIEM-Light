import { useState, useEffect, createElement } from "react";
import {
  Typography,
  Card,
  CardHeader,
  CardBody,
  Alert,
} from "@material-tailwind/react";
import {
  BellAlertIcon,
  CircleStackIcon,
  BellIcon,
  ExclamationTriangleIcon,
} from "@heroicons/react/24/solid";
import axios from "axios";
import endpoints from '@/apiConfig';

import { StatisticsCard } from "@/widgets/cards";

import { projectsTableData } from "@/data/projects-table-data"

export function Home() {
  const [showAlerts, setShowAlerts] = useState({
      active: false,
      color: "green",
      message: "Olá",
  });

  const [statistics, setStatistics] = useState({
    numAlerts: 0,
    numFeeds: 0,
    numUnseenAlerts: 0,
    numValues: 0,
    lastAlerts: []
  })
  
  useEffect(() => {
      const fetchData = async () => {
              const response = await axios.get(endpoints.getStats).then(function (response) {
                  setStatistics({
                      numFeeds: response.data.numFeeds,
                      numAlerts: response.data.numAlerts,
                      numUnseenAlerts: response.data.numUnseenAlerts,
                      numValues: response.data.numValues,
                      lastAlerts: response.data.lastAlerts,
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

  return (
    <div className="mt-6">
      <div className="mb-4 grid gap-y-10 gap-x-6 md:grid-cols-2 xl:grid-cols-4">
          <StatisticsCard
            key="1"
            color="gray"
            value={statistics["numUnseenAlerts"]}
            title="Alerts"
            icon={createElement(BellAlertIcon, {
              className: "w-6 h-6 text-white",
            })}
            footer={
              <Typography className="font-normal text-blue-gray-600">
                <strong className="text-green-500"></strong>
                &nbsp;{"Uncheck Alerts"}
              </Typography>
            }
          />
          <StatisticsCard
            key="2"
            color="gray"
            value={statistics["numAlerts"]}
            title="Total Alerts"
            icon={createElement(BellIcon, {
              className: "w-6 h-6 text-white",
            })}
            footer={
              <Typography className="font-normal text-blue-gray-600">
                <strong className="text-green-500"></strong>
                &nbsp;{"Total of alerts registered"}
              </Typography>
            }
          />
          <StatisticsCard
            key="3"
            color="gray"
            value={statistics["numFeeds"]}
            title="Feeds"
            icon={createElement(CircleStackIcon, {
              className: "w-6 h-6 text-white",
            })}
            footer={
              <Typography className="font-normal text-blue-gray-600">
                <strong className="text-green-500"></strong>
                &nbsp;{"Total of feeds consumed"}
              </Typography>
            }
          />
          <StatisticsCard
            key="4"
            color="gray"
            value={statistics["numValues"]}
            title="Data Collected"
            icon={createElement(ExclamationTriangleIcon, {
              className: "w-6 h-6 text-white",
            })}
            footer={
              <Typography className="font-normal text-blue-gray-600">
                <strong className="text-green-500"></strong>
                &nbsp;{"Number of IoCs collected"}
              </Typography>
            }
          />
        {/* {statisticsCardsData.map(({ icon, title, footer, ...rest }) => (
          <StatisticsCard
            key={title}
            {...rest}
            title={title}
            icon={createElement(icon, {
              className: "w-6 h-6 text-white",
            })}
            footer={
              <Typography className="font-normal text-blue-gray-600">
                <strong className={footer.color}>{footer.value}</strong>
                &nbsp;{footer.label}
              </Typography>
            }
          />
        ))} */}
      </div>
      {/* <div className="mb-6 grid grid-cols-1 gap-y-12 gap-x-6 md:grid-cols-2 xl:grid-cols-3">
        {statisticsChartsData.map((props) => (
          <StatisticsChart
            key={props.title}
            {...props}
            footer={
              <Typography
                variant="small"
                className="flex items-center font-normal text-blue-gray-600"
              >
                <ClockIcon strokeWidth={2} className="h-4 w-4 text-blue-gray-400" />
                &nbsp;{props.footer}
              </Typography>
            }
          />
        ))}
      </div> */}
      <div className="mb-4 grid grid-cols-1 gap-6 xl:grid-cols-1">
        <Card className="overflow-hidden xl:col-span-2 border border-blue-gray-100 shadow-sm">
          <CardHeader
            floated={false}
            shadow={false}
            color="transparent"
            className="m-0 flex items-center justify-between p-6"
          >
            <div>
              <Typography variant="h6" color="blue-gray" className="mb-1">
                Alerts
              </Typography>
              <Typography
                variant="small"
                className="flex items-center gap-1 font-normal text-blue-gray-600"
              >
                {/* <CheckCircleIcon strokeWidth={3} className="h-4 w-4 text-blue-gray-200" /> */}
                <strong>Last alerts created</strong>
              </Typography>
            </div>
          </CardHeader>
          <CardBody className="overflow-x-scroll px-0 pt-0 pb-2">
            <table className="w-full min-w-[640px] table-auto">
              <thead>
                <tr>
                  {["Alert Level", "Message"].map(
                    (el) => (
                      <th
                        key={el}
                        className="border-b border-blue-gray-50 py-3 px-6 text-left"
                      >
                        <Typography
                          variant="small"
                          className="text-[11px] font-medium uppercase text-blue-gray-400"
                        >
                          {el}
                        </Typography>
                      </th>
                    )
                  )}
                </tr>
              </thead>
              <tbody>
                {statistics["lastAlerts"].map(
                  ({ id, level, message }, key) => {
                    const className = `py-3 px-5 ${
                      key === statistics["lastAlerts"].length - 1
                        ? ""
                        : "border-b border-blue-gray-50"
                    }`;

                    return (
                      <tr key={id}>
                        <td className={className}>
                          {/* <div className="flex items-center gap-4"> */}
                            <Typography
                              variant="small"
                              color="blue-gray"
                              className="font-bold"
                            >
                              {level}
                            </Typography>
                          {/* </div> */}
                        </td>
                        <td className={className}>
                          <Typography
                            variant="small"
                            className="text-xs font-medium text-blue-gray-600"
                          >
                            {message}
                          </Typography>
                        </td>
                      </tr>
                    );
                  }
                )}
              </tbody>
            </table>
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
  );
}

export default Home;
