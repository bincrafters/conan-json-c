#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class JSONCConan(ConanFile):
    name = "json-c"
    version = "0.13.1"
    description = "JSON-C - A JSON implementation in C"
    url = "https://github.com/bincrafters/conan-json-c"
    homepage = "https://github.com/json-c/json-c"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "json-c.patch"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        file_name = "{0}-{1}-20180305".format(self.name, self.version)
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, file_name))
        extracted_dir = self.name + "-" + file_name
        os.rename(extracted_dir, self.source_subfolder)
        tools.patch(base_path=self.source_subfolder, patch_file="json-c.patch")

    def configure_cmake(self):
        cmake = CMake(self)
        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
