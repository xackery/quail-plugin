import bpy

class QuailHandlers:
    @staticmethod
    @bpy.app.handlers.persistent
    def load_handler(_):
        pass

    @staticmethod
    @bpy.app.handlers.persistent
    def save_pre_handler(_):
        pass

    @staticmethod
    def register():
        bpy.app.handlers.load_post.append(QuailHandlers.load_handler)
        bpy.app.handlers.save_pre.append(QuailHandlers.save_pre_handler)

    @staticmethod
    def unregister():
        bpy.app.handlers.save_pre.remove(QuailHandlers.save_pre_handler)
        bpy.app.handlers.load_post.remove(QuailHandlers.load_handler)
