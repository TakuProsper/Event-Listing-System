import React, { useContext } from 'react'
import { Link } from 'react-router-dom'
import AuthContext from '../context/AuthContext'



function LoginPage() {

  const {loginUser} = useContext(AuthContext)
  const handleSubmit = e => {
    e.preventDefault()
    const email = e.target.email.value
    const password = e.target.password.value

    email.length > 0 && loginUser(email, password)

    console.log(email)
    console.log(password)
   
  }

  return (
    <div>
      <>
  <section className="vh-150">
    <div className="container py-5 h-100">
      <div className="row d-flex justify-content-center align-items-center h-100">
        <div className="col col-xl-10 d-flex justify-content-center align-items-center">
          <div className="card" style={{ borderRadius: "1rem",width: '100%', maxWidth: '600px' }}>
            <div className="row g-0">
              <div className="col-md-12 col-lg-12 d-flex align-items-center" >
                <div className="card-body p-4 p-lg-5 text-black" >
                  <form onSubmit={handleSubmit} style={{ width: '100%' }}>

                  <div className="d-flex justify-content-center align-items-center mb-5 pb-1" style={{ width: '100%' }}>
                      <span className="h2 fw-bold mb-0">Welcome back 👋</span>
                  </div>

                    <h5
                      className="fw-normal mb-3 pb-3"
                      style={{ letterSpacing: 1 }}
                    >
                      Sign into your account
                    </h5>
                    <div className="form-outline mb-4">
                      <input
                        type="email"
                        id="form2Example17"
                        className="form-control form-control-lg"
                        name='email'
                      />
                      <label className="form-label" htmlFor="form2Example17">
                        Email address
                      </label>
                    </div>
                    <div className="form-outline mb-4">
                      <input
                        type="password"
                        id="form2Example27"
                        className="form-control form-control-lg"
                        name='password'
                      />
                      <label className="form-label" htmlFor="form2Example27">
                        Password
                      </label>
                    </div>
                    <div className="pt-1 mb-4">
                      <button
                        className="button btn btn-lg btn-block"
                        type="submit"
                      >
                        Login
                      </button>
                    </div>
                    <a className="small text-muted" href="#!">
                      Forgot password?
                    </a>
                    <p className="mb-5 pb-lg-2" style={{ color: "#393f81" }}>
                      Don't have an account?{" "}
                      <Link to="/register" style={{ color: "#393f81" }}>
                        Register Now 
                      </Link>
                    </p>
                    <a href="#!" className="small text-muted">
                      Terms of use.
                    </a>
                    <a href="#!" className="small text-muted">
                      Privacy policy
                    </a>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</>

    </div>
  )
}

export default LoginPage