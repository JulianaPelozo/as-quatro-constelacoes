import { BrowserRouter, Navigate, Route, Routes } from 'react-router'
import { rotaInicial, useAuth } from './auth'
import Exigir from './components/Exigir'
import ProvedorAuth from './components/ProvedorAuth'
import AdminInicio from './pages/admin/AdminInicio'
import AdminLayout from './pages/admin/AdminLayout'
import Login from './pages/Login'
import Painel from './pages/Painel'

function Inicio() {
  const { usuario } = useAuth()
  return <Navigate to={usuario ? rotaInicial(usuario) : '/entrar'} replace />
}

function Entrar() {
  const { usuario } = useAuth()
  return usuario ? <Navigate to={rotaInicial(usuario)} replace /> : <Login />
}

export default function App() {
  return (
    <ProvedorAuth>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Inicio />} />
          <Route path="/entrar" element={<Entrar />} />
          <Route
            path="/admin"
            element={
              <Exigir papel="administradora">
                <AdminLayout />
              </Exigir>
            }
          >
            <Route index element={<AdminInicio />} />
          </Route>
          <Route
            path="/painel"
            element={
              <Exigir>
                <Painel />
              </Exigir>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </ProvedorAuth>
  )
}
