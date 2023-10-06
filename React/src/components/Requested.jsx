import "../index.css"

export default function Requested(props) {
    return (
        <div className="requests_table" id="requests_table">
            <h1>Requested plants</h1>
            <table>
                <thead>
                    <tr>
                        <th>Plant name</th>
                        <th>Amount</th>
                        <th>Notes</th>
                        <th>Requested by</th>
                        <th>Date Posted</th>
                    </tr>
                </thead>
                <tbody>
                    {props.requests.map((request) => (
                        <tr key={(request.id)}>
                            <td>{request.plant_name}</td>
                            <td>{request.amount}</td>
                            <td>{request.notes}</td>
                            <td>{request.requested_by}</td>
                            <td>{request.date}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
