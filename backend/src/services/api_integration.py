"""
API Integration Layer for Military AI Simulation
Handles connections to external services including:
- Google Earth Engine for satellite imagery
- OpenStreetMap for mapping data
- Weather APIs for environmental conditions
- NASA satellite data for enhanced terrain
"""

import requests
import json
import logging
from datetime import datetime, timedelta
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
import os
from dataclasses import dataclass
import time
import sqlite3
from geopy.distance import geodesic
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Coordinates:
    """GPS coordinates with utility methods"""
    latitude: float
    longitude: float
    altitude: Optional[float] = None
    
    def to_dict(self):
        return {
            'lat': self.latitude,
            'lon': self.longitude,
            'alt': self.altitude
        }
    
    def distance_to(self, other):
        """Calculate distance to another coordinate in meters"""
        return geodesic((self.latitude, self.longitude), 
                       (other.latitude, other.longitude)).meters

@dataclass
class WeatherData:
    """Weather information structure"""
    temperature: float
    humidity: float
    wind_speed: float
    wind_direction: float
    visibility: float
    cloud_cover: float
    precipitation: float
    pressure: float
    timestamp: datetime

@dataclass
class SatelliteImage:
    """Satellite imagery data structure"""
    url: str
    coordinates: Coordinates
    zoom_level: int
    resolution: float
    timestamp: datetime
    source: str
    image_type: str

class APIIntegrationManager:
    """Main API integration management system"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.cache_db = "api_cache.db"
        self.rate_limits = {}
        self.session = None
        
        # Initialize API clients
        self.weather_client = WeatherAPIClient(self.config.get('weather', {}))
        self.maps_client = MapsAPIClient(self.config.get('maps', {}))
        self.satellite_client = SatelliteAPIClient(self.config.get('satellite', {}))
        self.earth_engine_client = EarthEngineClient(self.config.get('earth_engine', {}))
        
        # Initialize cache database
        self._init_cache_db()
        
        logger.info("API Integration Manager initialized")
    
    def _load_config(self, config_path):
        """Load API configuration"""
        default_config = {
            'weather': {
                'api_key': os.getenv('OPENWEATHER_API_KEY', ''),
                'base_url': 'https://api.openweathermap.org/data/2.5',
                'rate_limit': 60  # requests per minute
            },
            'maps': {
                'api_key': os.getenv('GOOGLE_MAPS_API_KEY', ''),
                'base_url': 'https://maps.googleapis.com/maps/api',
                'rate_limit': 1000
            },
            'satellite': {
                'nasa_api_key': os.getenv('NASA_API_KEY', ''),
                'usgs_username': os.getenv('USGS_USERNAME', ''),
                'usgs_password': os.getenv('USGS_PASSWORD', ''),
                'rate_limit': 100
            },
            'earth_engine': {
                'service_account_key': os.getenv('GEE_SERVICE_ACCOUNT_KEY', ''),
                'project_id': os.getenv('GEE_PROJECT_ID', ''),
                'rate_limit': 50
            }
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    def _init_cache_db(self):
        """Initialize SQLite cache database"""
        conn = sqlite3.connect(self.cache_db)
        cursor = conn.cursor()
        
        # Weather cache table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                latitude REAL,
                longitude REAL,
                timestamp TEXT,
                data TEXT,
                expiry TEXT
            )
        ''')
        
        # Satellite image cache table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS satellite_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                latitude REAL,
                longitude REAL,
                zoom_level INTEGER,
                timestamp TEXT,
                url TEXT,
                metadata TEXT,
                expiry TEXT
            )
        ''')
        
        # Map data cache table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS map_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                latitude REAL,
                longitude REAL,
                radius REAL,
                data_type TEXT,
                data TEXT,
                timestamp TEXT,
                expiry TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    async def get_comprehensive_area_data(self, center: Coordinates, 
                                        radius_km: float = 10.0) -> Dict[str, Any]:
        """Get comprehensive data for an area including weather, terrain, and satellite imagery"""
        tasks = [
            self.weather_client.get_weather_data(center),
            self.weather_client.get_weather_forecast(center, days=3),
            self.satellite_client.get_satellite_imagery(center, zoom_level=15),
            self.maps_client.get_terrain_data(center, radius_km),
            self.earth_engine_client.get_elevation_data(center, radius_km)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            'center': center.to_dict(),
            'radius_km': radius_km,
            'timestamp': datetime.now().isoformat(),
            'weather_current': results[0] if not isinstance(results[0], Exception) else None,
            'weather_forecast': results[1] if not isinstance(results[1], Exception) else None,
            'satellite_imagery': results[2] if not isinstance(results[2], Exception) else None,
            'terrain_data': results[3] if not isinstance(results[3], Exception) else None,
            'elevation_data': results[4] if not isinstance(results[4], Exception) else None,
            'errors': [str(r) for r in results if isinstance(r, Exception)]
        }

class WeatherAPIClient:
    """OpenWeatherMap API client"""
    
    def __init__(self, config: Dict[str, Any]):
        self.api_key = config.get('api_key')
        self.base_url = config.get('base_url')
        self.rate_limit = config.get('rate_limit', 60)
        self.last_request_time = 0
        
    async def get_weather_data(self, coordinates: Coordinates) -> Optional[WeatherData]:
        """Get current weather data for coordinates"""
        if not self.api_key:
            logger.warning("OpenWeatherMap API key not configured")
            return None
        
        # Check rate limiting
        if not self._check_rate_limit():
            logger.warning("Rate limit exceeded for weather API")
            return None
        
        url = f"{self.base_url}/weather"
        params = {
            'lat': coordinates.latitude,
            'lon': coordinates.longitude,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_weather_data(data)
                    else:
                        logger.error(f"Weather API error: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error fetching weather data: {e}")
            return None
    
    async def get_weather_forecast(self, coordinates: Coordinates, 
                                 days: int = 5) -> Optional[List[WeatherData]]:
        """Get weather forecast for coordinates"""
        if not self.api_key:
            return None
        
        if not self._check_rate_limit():
            return None
        
        url = f"{self.base_url}/forecast"
        params = {
            'lat': coordinates.latitude,
            'lon': coordinates.longitude,
            'appid': self.api_key,
            'units': 'metric',
            'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [self._parse_weather_data(item) for item in data['list']]
                    else:
                        logger.error(f"Weather forecast API error: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error fetching weather forecast: {e}")
            return None
    
    def _parse_weather_data(self, data: Dict) -> WeatherData:
        """Parse weather data from API response"""
        main = data.get('main', {})
        wind = data.get('wind', {})
        clouds = data.get('clouds', {})
        rain = data.get('rain', {})
        
        return WeatherData(
            temperature=main.get('temp', 0),
            humidity=main.get('humidity', 0),
            wind_speed=wind.get('speed', 0),
            wind_direction=wind.get('deg', 0),
            visibility=data.get('visibility', 10000) / 1000,  # Convert to km
            cloud_cover=clouds.get('all', 0),
            precipitation=rain.get('1h', 0),
            pressure=main.get('pressure', 1013),
            timestamp=datetime.fromtimestamp(data.get('dt', time.time()))
        )
    
    def _check_rate_limit(self) -> bool:
        """Check if we can make a request within rate limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < 60 / self.rate_limit:
            return False
        
        self.last_request_time = current_time
        return True

class SatelliteAPIClient:
    """NASA and USGS satellite data client"""
    
    def __init__(self, config: Dict[str, Any]):
        self.nasa_api_key = config.get('nasa_api_key')
        self.usgs_username = config.get('usgs_username')
        self.usgs_password = config.get('usgs_password')
        self.rate_limit = config.get('rate_limit', 100)
        self.last_request_time = 0
        
    async def get_satellite_imagery(self, coordinates: Coordinates, 
                                  zoom_level: int = 12) -> Optional[SatelliteImage]:
        """Get satellite imagery for coordinates"""
        # Try NASA GIBS first, then fallback to other sources
        image = await self._get_nasa_gibs_imagery(coordinates, zoom_level)
        
        if not image:
            image = await self._get_landsat_imagery(coordinates, zoom_level)
        
        return image
    
    async def _get_nasa_gibs_imagery(self, coordinates: Coordinates, 
                                   zoom_level: int) -> Optional[SatelliteImage]:
        """Get imagery from NASA GIBS"""
        if not self.nasa_api_key:
            logger.warning("NASA API key not configured")
            return None
        
        # NASA GIBS WMTS service
        base_url = "https://map1.vis.earthdata.nasa.gov/wmts/1.0.0"
        layer = "MODIS_Aqua_CorrectedReflectance_TrueColor"
        
        # Calculate tile coordinates
        tile_x, tile_y = self._lat_lon_to_tile(
            coordinates.latitude, coordinates.longitude, zoom_level
        )
        
        url = f"{base_url}/{layer}/default/2023-01-01/GoogleMapsCompatible_Level{zoom_level}/{zoom_level}/{tile_x}/{tile_y}.jpg"
        
        return SatelliteImage(
            url=url,
            coordinates=coordinates,
            zoom_level=zoom_level,
            resolution=self._calculate_resolution(zoom_level),
            timestamp=datetime.now(),
            source="NASA_GIBS",
            image_type="true_color"
        )
    
    async def _get_landsat_imagery(self, coordinates: Coordinates, 
                                 zoom_level: int) -> Optional[SatelliteImage]:
        """Get Landsat imagery from USGS"""
        # This would require USGS API authentication and complex queries
        # For now, return a placeholder
        logger.info("Landsat imagery would be fetched here")
        return None
    
    def _lat_lon_to_tile(self, lat: float, lon: float, zoom: int) -> tuple:
        """Convert latitude/longitude to tile coordinates"""
        lat_rad = np.radians(lat)
        n = 2 ** zoom
        x = int((lon + 180) / 360 * n)
        y = int((1 - np.arcsinh(np.tan(lat_rad)) / np.pi) / 2 * n)
        return x, y
    
    def _calculate_resolution(self, zoom_level: int) -> float:
        """Calculate resolution in meters per pixel for zoom level"""
        # Approximate resolution at equator
        return 156543.03392 * np.cos(0) / (2 ** zoom_level)

class MapsAPIClient:
    """Google Maps API client"""
    
    def __init__(self, config: Dict[str, Any]):
        self.api_key = config.get('api_key')
        self.base_url = config.get('base_url')
        self.rate_limit = config.get('rate_limit', 1000)
        self.last_request_time = 0
    
    async def get_terrain_data(self, coordinates: Coordinates, 
                             radius_km: float) -> Optional[Dict[str, Any]]:
        """Get terrain and elevation data for area"""
        if not self.api_key:
            logger.warning("Google Maps API key not configured")
            return None
        
        # Get elevation data
        elevation_data = await self._get_elevation_profile(coordinates, radius_km)
        
        # Get nearby places of interest
        places_data = await self._get_nearby_places(coordinates, radius_km)
        
        return {
            'center': coordinates.to_dict(),
            'radius_km': radius_km,
            'elevation_data': elevation_data,
            'places': places_data,
            'timestamp': datetime.now().isoformat()
        }
    
    async def _get_elevation_profile(self, coordinates: Coordinates, 
                                   radius_km: float) -> Optional[List[Dict]]:
        """Get elevation profile for area"""
        # Create a grid of points around the center
        points = []
        steps = 10
        lat_step = radius_km / 111.32 / steps  # Approximate km to degrees
        lon_step = radius_km / (111.32 * np.cos(np.radians(coordinates.latitude))) / steps
        
        for i in range(-steps, steps + 1):
            for j in range(-steps, steps + 1):
                lat = coordinates.latitude + i * lat_step
                lon = coordinates.longitude + j * lon_step
                points.append(f"{lat},{lon}")
        
        # Google Elevation API
        url = f"{self.base_url}/elevation/json"
        params = {
            'locations': '|'.join(points[:500]),  # API limit
            'key': self.api_key
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('results', [])
                    else:
                        logger.error(f"Elevation API error: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error fetching elevation data: {e}")
            return None
    
    async def _get_nearby_places(self, coordinates: Coordinates, 
                               radius_km: float) -> Optional[List[Dict]]:
        """Get nearby places of interest"""
        url = f"{self.base_url}/place/nearbysearch/json"
        params = {
            'location': f"{coordinates.latitude},{coordinates.longitude}",
            'radius': int(radius_km * 1000),  # Convert to meters
            'type': 'establishment',
            'key': self.api_key
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('results', [])
                    else:
                        logger.error(f"Places API error: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error fetching places data: {e}")
            return None

class EarthEngineClient:
    """Google Earth Engine API client"""
    
    def __init__(self, config: Dict[str, Any]):
        self.service_account_key = config.get('service_account_key')
        self.project_id = config.get('project_id')
        self.rate_limit = config.get('rate_limit', 50)
        self.authenticated = False
        
        # Note: Actual Earth Engine authentication would require the ee library
        # and proper service account setup
    
    async def get_elevation_data(self, coordinates: Coordinates, 
                               radius_km: float) -> Optional[Dict[str, Any]]:
        """Get high-resolution elevation data from Earth Engine"""
        if not self.authenticated:
            logger.warning("Earth Engine not authenticated")
            return None
        
        # This would use the actual Earth Engine Python API
        # For now, return simulated data
        return {
            'center': coordinates.to_dict(),
            'radius_km': radius_km,
            'dataset': 'SRTM30',
            'resolution': 30,  # meters
            'min_elevation': 100,
            'max_elevation': 500,
            'mean_elevation': 300,
            'timestamp': datetime.now().isoformat(),
            'note': 'Simulated data - requires Earth Engine setup'
        }
    
    async def get_landcover_data(self, coordinates: Coordinates, 
                               radius_km: float) -> Optional[Dict[str, Any]]:
        """Get land cover classification data"""
        if not self.authenticated:
            return None
        
        # Simulated land cover data
        return {
            'center': coordinates.to_dict(),
            'radius_km': radius_km,
            'dataset': 'MODIS_Land_Cover',
            'classes': {
                'forest': 45.2,
                'grassland': 30.1,
                'urban': 15.3,
                'water': 9.4
            },
            'timestamp': datetime.now().isoformat(),
            'note': 'Simulated data - requires Earth Engine setup'
        }

class CacheManager:
    """Manages API response caching to reduce external requests"""
    
    def __init__(self, db_path: str = "api_cache.db"):
        self.db_path = db_path
    
    def get_cached_weather(self, coordinates: Coordinates, 
                          max_age_minutes: int = 30) -> Optional[WeatherData]:
        """Get cached weather data if available and fresh"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        expiry_time = datetime.now() - timedelta(minutes=max_age_minutes)
        
        cursor.execute('''
            SELECT data FROM weather_cache 
            WHERE latitude = ? AND longitude = ? 
            AND timestamp > ?
            ORDER BY timestamp DESC
            LIMIT 1
        ''', (coordinates.latitude, coordinates.longitude, expiry_time.isoformat()))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            try:
                data = json.loads(result[0])
                return WeatherData(**data)
            except Exception as e:
                logger.error(f"Error parsing cached weather data: {e}")
        
        return None
    
    def cache_weather_data(self, coordinates: Coordinates, 
                          weather_data: WeatherData, 
                          cache_duration_hours: int = 1):
        """Cache weather data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        expiry = datetime.now() + timedelta(hours=cache_duration_hours)
        
        cursor.execute('''
            INSERT INTO weather_cache 
            (latitude, longitude, timestamp, data, expiry)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            coordinates.latitude,
            coordinates.longitude,
            datetime.now().isoformat(),
            json.dumps(weather_data.__dict__, default=str),
            expiry.isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def cleanup_expired_cache(self):
        """Remove expired cache entries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        current_time = datetime.now().isoformat()
        
        # Clean up all cache tables
        tables = ['weather_cache', 'satellite_cache', 'map_cache']
        for table in tables:
            cursor.execute(f'DELETE FROM {table} WHERE expiry < ?', (current_time,))
        
        conn.commit()
        conn.close()

# Example usage and testing
async def main():
    """Example usage of the API integration system"""
    # Initialize the integration manager
    api_manager = APIIntegrationManager()
    
    # Define test coordinates (e.g., military base location)
    test_coords = Coordinates(latitude=35.0844, longitude=-106.6504)  # Kirtland AFB
    
    try:
        # Get comprehensive area data
        area_data = await api_manager.get_comprehensive_area_data(
            test_coords, radius_km=15.0
        )
        
        print("Area Data Retrieved:")
        print(json.dumps(area_data, indent=2, default=str))
        
        # Get specific weather data
        weather = await api_manager.weather_client.get_weather_data(test_coords)
        if weather:
            print(f"\nCurrent Weather:")
            print(f"Temperature: {weather.temperature}°C")
            print(f"Wind Speed: {weather.wind_speed} m/s")
            print(f"Visibility: {weather.visibility} km")
        
        # Get satellite imagery
        satellite_img = await api_manager.satellite_client.get_satellite_imagery(
            test_coords, zoom_level=15
        )
        if satellite_img:
            print(f"\nSatellite Image URL: {satellite_img.url}")
            print(f"Resolution: {satellite_img.resolution:.2f} m/pixel")
        
    except Exception as e:
        logger.error(f"Error in API integration example: {e}")

if __name__ == "__main__":
    asyncio.run(main())