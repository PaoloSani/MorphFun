const Button = ({ stringToDisplay, functionToTrigger, id }) => {
  return <button id={id} onClick={functionToTrigger}>{stringToDisplay}</button>;
};

export default Button;
