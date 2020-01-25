import React from 'react';
import {Line} from 'react-chartjs-2';

const WEEKDAYS = [
    "So",
    "Mo",
    "Di",
    "Mi",
    "Do",
    "Fr",
    "Sa"
]

export default class ActivityChart extends React.Component {

    render() {
        const unit = this.props.unit;
        let groups;
        let labels;
        switch (unit) {
            case 'hour':
                groups =[...Array(24).keys()];
                labels = groups.map(x => `${x} Uhr`);
                break;
            case 'weekday':
                groups = [...Array(7).keys()];
                labels = groups.map(x => WEEKDAYS[x]);
                break;
            default:
                throw new Error(`Unsupported unit ${unit}`);
        }

        const data = {
            labels: labels,
            options: {
				scales: {
					xAxes: [{
						type: 'time',
                        time: {
                            unit: unit
                        }
                    }]
				}
			},
            datasets: [
              {
                data: this.props.data
              }
            ]
           
        }

        const options = {
            legend: {
                display: false
            },
        }

        return (
            <Line data={data} options={options} height={50} />
        );
    }
}
