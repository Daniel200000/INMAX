# 🚀 Desarrollo Local - Web Avisadores

## Inicio Rápido

### Opción 1: Script Automático (Recomendado)

**Windows:**
```bash
start-dev.bat
```

**Linux/macOS:**
```bash
chmod +x start-dev.sh
./start-dev.sh
```

### Opción 2: Comandos Manuales

1. **Configurar variables de entorno:**
   ```bash
   cp env.example .env
   ```

2. **Iniciar servicios:**
   ```bash
   docker-compose up --build -d
   ```

3. **Verificar que todo esté funcionando:**
   ```bash
   docker-compose ps
   ```

## 🌐 URLs de Acceso

- **Frontend (React)**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MongoDB Express**: http://localhost:8081

## 📋 Funcionalidades del Dashboard

### ✅ Implementadas y Funcionando

1. **Dashboard Principal**
   - Búsqueda de campañas en tiempo real
   - Filtros por estado y fecha
   - Auto-refresh cada 30 segundos
   - Estadísticas con tendencias

2. **Componentes Interactivos**
   - Barra de búsqueda con debounce
   - Panel de filtros desplegable
   - Acciones rápidas con gradientes
   - Gráficos SVG personalizados

3. **Métricas de Rendimiento**
   - CTR (Click Through Rate)
   - CPC (Cost Per Click)
   - CPM (Cost Per Mille)
   - Tasa de conversión

4. **Datos de Demostración**
   - 5 campañas de ejemplo
   - Diferentes estados (activa, pausada, finalizada)
   - Métricas realistas
   - Ubicaciones geográficas

## 🎨 Diseño y Colores

### Esquema de Colores Corporativo
- **Azul Principal**: #2b6cb0 (Botones primarios)
- **Azul Oscuro**: #1a365d (Títulos)
- **Gris Claro**: #f8f9fa (Fondo)
- **Blanco**: #ffffff (Tarjetas)

### Características Visuales
- Diseño limpio y profesional
- Gradientes sutiles
- Animaciones suaves
- Responsive design
- Iconos emoji para mejor UX

## 🔧 Comandos Útiles

### Ver logs en tiempo real
```bash
docker-compose logs -f
```

### Ver logs de un servicio específico
```bash
docker-compose logs -f frontend
docker-compose logs -f backend
```

### Reiniciar un servicio
```bash
docker-compose restart frontend
docker-compose restart backend
```

### Detener todos los servicios
```bash
docker-compose down
```

### Limpiar volúmenes (CUIDADO: Borra datos)
```bash
docker-compose down -v
```

## 🐛 Solución de Problemas

### Puerto ya en uso
Si el puerto 3000 o 8000 está ocupado:
```bash
# Cambiar puertos en docker-compose.yml
# O matar el proceso que usa el puerto
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Error de permisos en Linux/macOS
```bash
sudo chmod +x start-dev.sh
```

### Limpiar caché de Docker
```bash
docker system prune -a
docker-compose up --build --force-recreate
```

## 📱 Pruebas en Dispositivos Móviles

1. **En la misma red local:**
   - Encuentra tu IP local: `ipconfig` (Windows) o `ifconfig` (Linux/macOS)
   - Accede desde móvil: `http://TU_IP:3000`

2. **Usando ngrok (túnel público):**
   ```bash
   # Instalar ngrok
   npm install -g ngrok
   
   # Crear túnel
   ngrok http 3000
   ```

## 🎯 Próximos Pasos

1. **Integrar con backend real** (actualmente usa datos mock)
2. **Implementar autenticación** real
3. **Agregar más tipos de gráficos**
4. **Implementar notificaciones** en tiempo real
5. **Agregar exportación** de datos

## 📞 Soporte

Si encuentras algún problema:
1. Revisa los logs: `docker-compose logs -f`
2. Verifica que los puertos estén libres
3. Reinicia los servicios: `docker-compose restart`
4. Limpia y reconstruye: `docker-compose up --build --force-recreate`

¡El módulo de campañas está listo para usar! 🎉
