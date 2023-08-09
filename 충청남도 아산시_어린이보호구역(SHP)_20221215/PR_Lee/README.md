# README.md

shp 파일 전체 완성은 되지 않았고, 코드 테스트 필요.

```bash
    [종속성]
    import geopandas
    import shapely.geometry
    
    [디렉토리 구조]
    - parking
    - shp
        - busstop.shp
        - crossedge.shp
        - crosswalk.shp
        - fireplug.shp
        - RDL_SCHO_AS.shp
```

## 테스트 코드

```python
if __name__ == '__main__':
    import geopandas as gpd
    from shapely.geometry import Point
    
    pk = parking()
    output = pk.parking_readout(10.1, 10.2, 8) # 위도, 경도, 시간(단위: 시)
    print(output)

```
