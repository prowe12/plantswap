import "../index.css"

export default function Available(props) {

    return (
        <div className="plants_table" id="plants_table">
            <h1>Available plants</h1>
            <table>
                <thead>
                    <tr>
                        <th>Plant name</th>
                        <th>Amount</th>
                        <th>Description</th>
                        <th>Available Now?</th>
                        <th>Shared by</th>
                        <th>Date Posted</th>
                    </tr>
                </thead>
                <tbody>
                    {props.shares.map((share) => (
                        <tr key={(share.id)}>
                            <td>{share.plant_name}</td>
                            <td>{share.amount}</td>
                            <td>{share.description}</td>
                            <td>{share.is_available_now ? 'Yes' : 'No'} </td>
                            <td>{share.shared_by}</td>
                            <td>{share.date}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
