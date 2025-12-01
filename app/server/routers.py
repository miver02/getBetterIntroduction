from . import get_apirouters_data, logger


MODELS_ROUTES = get_apirouters_data().get("MODELS_ROUTES")
USERS_ROUTES = get_apirouters_data().get("USERS_ROUTES")

class Routers:
    def __init__(self):
        pass

    def get_all_routes_summary(self):
        """获取所有路由摘要"""
        all_routes = []
        
        for module_name, module_config in [("model", MODELS_ROUTES),  ("users", USERS_ROUTES)]:
            prefix = module_config["prefix"]
            for endpoint_name, endpoint_config in module_config["endpoints"].items():
                all_routes.append({
                    "module": module_name,
                    "method": endpoint_config["method"],
                    "full_path": prefix + endpoint_config["path"],
                    "endpoint": endpoint_name,
                    "summary": endpoint_config["summary"]
                })
        
        return all_routes

    def logger_route_summary(self):
        """打印路由摘要表"""
        routes = self.get_all_routes_summary()
        logger.info("=" * 80)
        logger.info("API 路由概览")
        logger.info("=" * 80)
        logger.info(f"{'模块':<10} {'方法':<6} {'路径':<30} {'端点':<20} {'摘要'}")
        logger.info("-" * 80)
        
        for route in routes:
            logger.info(f"{route['module']:<10} {route['method']:<6} {route['full_path']:<30} {route['endpoint']:<20} {route['summary']}")
