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
                    {props.shares}
                </tbody>
            </table>

            {/* 
            <p>
                <a href="/register">Register</a>
            </p>
            <p>
                <a href="/login">Login</a>
            </p> */}
        </div>
    );
}
