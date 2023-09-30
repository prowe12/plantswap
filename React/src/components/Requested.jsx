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
                    {props.requests}
                </tbody>
            </table>

        </div>
    );
}
