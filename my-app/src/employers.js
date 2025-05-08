import React, { useEffect, useState } from "react";

function Employers() {
    const [employers, setEmployers] = useState([]);
    const [loading, setLoading] = useState(true);

useEffect(() => {
    fetch("http://localhost:8000/employers")
      .then((response) => response.json())
      .then((data) => {
        setEmployers(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching employers:", error);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h1>Employers</h1>
      <ul>
        {employers.map((employer) => (
          <li key={employer.employer_id}>
            {employer.employer_name} — {employer.username}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Employers;