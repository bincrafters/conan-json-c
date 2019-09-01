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
    default_options = {'shared': False, 'fPIC': True}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        file_name = "{0}-{1}-20180305".format(self.name, self.version)
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, file_name))
        extracted_dir = self.name + "-" + file_name
        os.rename(extracted_dir, self._source_subfolder)
        tools.patch(base_path=self._source_subfolder, patch_file="json-c.patch")

    def _configure_cmake(self):
        if tools.cross_building(self.settings) and self.settings.os != "Windows":
            host = tools.get_gnu_triplet(str(self.settings.os), str(self.settings.arch))
            tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"),
                                  "execute_process(COMMAND ./configure ",
                                  "execute_process(COMMAND ./configure --host %s " % host)
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
