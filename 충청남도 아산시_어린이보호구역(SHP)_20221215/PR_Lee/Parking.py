class parking:
    '''
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
    '''
    def __init__(self):
        self.busstop = gpd.read_file("./shp/busstop.shp")
        self.crossedge = gpd.read_file("./shp/crossedge.shp")
        self.crosswalk = gpd.read_file("./shp/crosswalk.shp")
        self.fireplug = gpd.read_file("./shp/fireplug.shp")
        self.RDL_SCHO_AS = gpd.read_file("./shp/RDL_SCHO_AS.shp")

    def parking_readout(self, x:float, y:float, time:int) -> tuple:
        '''(위도, 경도) 바탕 주정차 판독 함수
        @param x : 위도, float
        @param y : 경도, float
        @param time : 시간, 단위는 '시'로 입력, int
        @return tuple : (bool, int)
            bool : 1(주정차), 0(일반차량)
            int : 위반 포인트(-1: 위반하지 않음, 0:어린이보호구역, 1:버스정류장, 2:교차로, 3:횡단보도, 4:소화전)
        '''

        xy_data = gpd.GeoDataFrame({"geometry" : [Point(x, y)]})
        xy_data.crs = "EPSG:4326"

        if self.EPSG_Set(xy_data, self.RDL_SCHO_AS) and (time > 8 and time < 20):
            return (True, 0)
        
        if self.EPSG_Set(xy_data, self.busstop):
            return (True, 1)

        if self.EPSG_Set(xy_data, self.crossedge):
            return (True, 2)

        if self.EPSG_Set(xy_data, self.crosswalk):
            return (True, 3)

        if self.EPSG_Set(xy_data, self.fireplug):
            return (True, 4)

        return (0, -1)
        
    def EPSG_Set(self, gdf_data, gpd_data) -> bool:
        '''shp파일 생성시 EPSG 잘못 설정해서 하는 전처리 함수
        @param gdf_data : 현재 위치 데이터, GeoDataFrame
        @param gpd_data : 위반 구역 데이터, GeoDataFrame
        @return bool : 1(주정차), 0(일반차량), bool
        '''
        try:
            gdf_set = gdf_data.to_crs("EPSG:5181")
            check_list = gpd.sjoin(gdf_set, gpd_data)
        except:
            gdf_set = gdf_data.to_crs("EPSG:5186")
            check_list = gpd.sjoin(gdf_set, gpd_data)

        return bool(len(check_list))

if __name__ == '__main__':
    import geopandas as gpd
    from shapely.geometry import Point
    
    pk = parking()
    output = pk.parking_readout(10.1, 10.2, 8) # 위도, 경도, 시간(단위: 시)
    print(output)
