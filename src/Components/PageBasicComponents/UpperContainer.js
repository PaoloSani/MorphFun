const UpperContainer = () => {
  return (
    <nav className="navbar">
      <h1 className="title-header" style={{ fontSize: "15rem" }}>
        MORPH FUN
      </h1>
      <div className="links">
        <a
          rel="noopener noreferrer"
          style={{
            color: "white",
            backgroundColor: "rgb(237, 36, 129)",
            borderRadius: "0.5rem",
            fontSize: "8rem",
            marginLeft: "7rem"
            
          }}
          href="https://github.com/PaoloSani/MorphFun"
          target="_blank"
        >
          About
        </a>
      </div>
    </nav>
  );
};

export default UpperContainer;
