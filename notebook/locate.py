import pkgutil

package_name = "cellpose"
package_path = pkgutil.get_loader(package_name).get_filename()
print(package_path)