import { useEffect, useState } from "react";
import { useHistory } from "react-router";

function HeroPowerForm() {
  const [heroes, setHeroes] = useState([]);
  const [powers, setPowers] = useState([]);
  const [heroId, setHeroId] = useState("");
  const [powerId, setPowerId] = useState("");
  const [strength, setStrength] = useState("");
  const [formErrors, setFormErrors] = useState([]);
  const history = useHistory();

  useEffect(() => {
    fetch("/heroes")
      .then((r) => r.json())
      .then(setHeroes);
  }, []);

  useEffect(() => {
    fetch("/powers")
      .then((r) => r.json())
      .then(setPowers);
  }, []);

  function handleSubmit(e) {
    e.preventDefault();
    const formData = {
      hero_id: heroId,
      power_id: powerId,
      strength,
    };
    fetch("/hero_powers", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    }).then((r) => {
      if (r.ok) {
        history.push(`/heroes/${heroId}`);
      } else {
        r.json().then((err) => setFormErrors(err.errors));
      }
    });
  }

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="power_id">Power:</label>
      <select
        id="power_id"
        name="power_id"
        value={powerId}
        onChange={(e) => setPowerId(e.target.value)}
      >
        <option value="">Select a power</option>
        {powers.map((power) => (
          <option key={power.id} value={power.id}>
            {power.name}
          </option>
        ))}
      </select>
      <label htmlFor="hero_id">Hero:</label>
      <select
        id="hero_id"
        name="hero_id"
        value={heroId}
        onChange={(e) => setHeroId(e.target.value)}
      >
        <option value="">Select a hero</option>
        {heroes.map((hero) => (
          <option key={hero.id} value={hero.id}>
            {hero.name}
          </option>
        ))}
      </select>
      <label htmlFor="strength">Strength:</label>
      <input
        type="text"
        id="strength"
        name="strength"
        value={strength}
        onChange={(e) => setStrength(e.target.value)}
      />
      {formErrors.length > 0
        ? formErrors.map((err) => (
            <p key={err} style={{ color: "red" }}>
              {err}
            </p>
          ))
        : null}
      <button type="submit">Add Hero Power</button>
    </form>
  );
}

export default HeroPowerForm;
